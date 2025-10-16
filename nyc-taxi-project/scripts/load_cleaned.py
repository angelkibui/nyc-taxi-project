# scripts/load_cleaned.py
"""
Load a cleaned CSV named cleaned_trips.csv (put it in /data or repo root).
This script:
 - creates the SQLite DB (nyc_taxi.db) if missing
 - creates schema (executes schema.sql)
 - inserts payment types, locations, time_dim entries
 - inserts trips in batches
 - computes derived features (avg_speed_kmph, fare_per_km) if not present
"""

import os
import csv
import sqlite3
from datetime import datetime
from dateutil import parser

DB_FILE = os.getenv("DB_FILE", "nyc_taxi.db")
CSV_PATH = os.getenv("CLEANED_CSV", "cleaned_trips.csv")
SCHEMA_FILE = os.getenv("SCHEMA_FILE", "schema.sql")
BATCH = 500

def exec_schema(conn):
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn.executescript(sql)

def parse_row(row):
    # Expected headers: trip_id,pickup_datetime,dropoff_datetime,pickup_lat,pickup_lon,dropoff_lat,dropoff_lon,trip_duration_secs,trip_distance_km,fare_amount,tip_amount,passenger_count,payment_type
    pickup_dt = parser.parse(row["pickup_datetime"])
    dropoff_dt = parser.parse(row["dropoff_datetime"])
    duration = int(float(row["trip_duration_secs"]))
    distance = float(row["trip_distance_km"])
    fare = float(row["fare_amount"])
    tip = float(row.get("tip_amount") or 0.0)
    avg_speed = None
    fare_per_km = None
    if duration > 0:
        hours = duration / 3600.0
        if hours > 0:
            avg_speed = distance / hours
    if distance > 0:
        fare_per_km = fare / distance

    return {
        "raw_trip_id": row.get("trip_id"),
        "pickup_datetime": pickup_dt.isoformat(sep=' '),
        "dropoff_datetime": dropoff_dt.isoformat(sep=' '),
        "trip_duration_secs": duration,
        "trip_distance_km": distance,
        "fare_amount": fare,
        "tip_amount": tip,
        "passenger_count": int(float(row.get("passenger_count") or 0)),
        "payment_type": row.get("payment_type") or "unknown",
        "pickup_lat": round(float(row["pickup_lat"]), 6),
        "pickup_lon": round(float(row["pickup_lon"]), 6),
        "dropoff_lat": round(float(row["dropoff_lat"]), 6),
        "dropoff_lon": round(float(row["dropoff_lon"]), 6),
        "avg_speed_kmph": avg_speed,
        "fare_per_km": fare_per_km,
        "pickup_dt_obj": pickup_dt,
        "dropoff_dt_obj": dropoff_dt
    }

def upsert_payment_types(conn, payments):
    cur = conn.cursor()
    for p in payments:
        cur.execute("INSERT OR IGNORE INTO payment_types(payment_type) VALUES (?)", (p,))
    conn.commit()

def upsert_locations(conn, locs):
    cur = conn.cursor()
    # Using many inserts with OR IGNORE
    cur.executemany("INSERT OR IGNORE INTO locations(latitude, longitude) VALUES (?, ?)", locs)
    conn.commit()

def upsert_time_dim(conn, dts):
    cur = conn.cursor()
    # dts are datetime objects
    rows = [(dt.isoformat(sep=' '), dt.year, dt.month, dt.day, dt.hour, dt.weekday()) for dt in dts]
    cur.executemany("INSERT OR IGNORE INTO time_dim(dt, year, month, day, hour, weekday) VALUES (?, ?, ?, ?, ?, ?)", rows)
    conn.commit()

def get_location_map(conn):
    cur = conn.cursor()
    cur.execute("SELECT location_id, latitude, longitude FROM locations")
    return { (round(row[1],6), round(row[2],6)): row[0] for row in cur.fetchall() }

def get_time_map(conn):
    cur = conn.cursor()
    cur.execute("SELECT time_id, dt FROM time_dim")
    return { row[1]: row[0] for row in cur.fetchall() }

def load_trips(conn, parsed_rows):
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO trips (
       raw_trip_id, pickup_location_id, dropoff_location_id,
       pickup_time_id, dropoff_time_id, pickup_datetime, dropoff_datetime,
       trip_duration_secs, trip_distance_km, fare_amount, tip_amount,
       passenger_count, payment_type, avg_speed_kmph, fare_per_km
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    batch = []
    loc_map = get_location_map(conn)
    time_map = get_time_map(conn)

    for r in parsed_rows:
        pk = loc_map.get((r["pickup_lat"], r["pickup_lon"]))
        dk = loc_map.get((r["dropoff_lat"], r["dropoff_lon"]))
        if pk is None or dk is None:
            # skip if location not found (shouldn't happen)
            continue
        ptime = time_map.get(r["pickup_datetime"])
        dtime = time_map.get(r["dropoff_datetime"])
        batch.append((
            r["raw_trip_id"], pk, dk, ptime, dtime,
            r["pickup_datetime"], r["dropoff_datetime"],
            r["trip_duration_secs"], r["trip_distance_km"], r["fare_amount"], r["tip_amount"],
            r["passenger_count"], r["payment_type"], r["avg_speed_kmph"], r["fare_per_km"]
        ))
        if len(batch) >= BATCH:
            cur.executemany(insert_sql, batch)
            conn.commit()
            batch.clear()
    if batch:
        cur.executemany(insert_sql, batch)
        conn.commit()

def main():
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}. Put cleaned_trips.csv in the repo root or set CLEANED_CSV env var.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    exec_schema(conn)

    parsed_rows = []
    payments = set()
    locs = set()
    times = set()

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rec = parse_row(row)
            except Exception as e:
                print("Skipping row due to parse error:", e)
                continue
            parsed_rows.append(rec)
            payments.add(rec["payment_type"])
            locs.add((rec["pickup_lat"], rec["pickup_lon"]))
            locs.add((rec["dropoff_lat"], rec["dropoff_lon"]))
            times.add(rec["pickup_dt_obj"])
            times.add(rec["dropoff_dt_obj"])

    # upsert dims
    upsert_payment_types(conn, payments)
    upsert_locations(conn, list(locs))
    upsert_time_dim(conn, list(times))

    # reload maps and insert trips
    load_trips(conn, parsed_rows)
    conn.close()
    print("Load completed - records inserted into", DB_FILE)

if __name__ == "__main__":
    main()
