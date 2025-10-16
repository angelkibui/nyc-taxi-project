# backend/app.py
# Single-file backend combining database, data processing, and algorithm logic

import sqlite3
import math

# ---------- DATABASE SETUP ----------
def create_database():
    conn = sqlite3.connect("nyc_taxi.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup_datetime TEXT,
            dropoff_datetime TEXT,
            trip_distance REAL,
            fare_amount REAL,
            tip_amount REAL,
            fare_per_km REAL
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database and table created successfully.")

def insert_sample_data():
    conn = sqlite3.connect("nyc_taxi.db")
    cursor = conn.cursor()

    sample_data = [
        ("2024-01-01 08:00:00", "2024-01-01 08:30:00", 10.5, 25.0, 3.0, 25.0/10.5),
        ("2024-01-01 09:15:00", "2024-01-01 09:45:00", 8.2, 22.0, 2.5, 22.0/8.2),
        ("2024-01-01 10:00:00", "2024-01-01 10:05:00", 1.2, 18.0, 0.5, 18.0/1.2),  # outlier
        ("2024-01-01 11:00:00", "2024-01-01 11:20:00", 6.0, 14.0, 1.0, 14.0/6.0),
        ("2024-01-01 12:00:00", "2024-01-01 12:35:00", 12.0, 30.0, 5.0, 30.0/12.0)
    ]

    cursor.executemany("""
        INSERT INTO trips (pickup_datetime, dropoff_datetime, trip_distance, fare_amount, tip_amount, fare_per_km)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()
    print("✅ Sample data inserted successfully.")


# ---------- CUSTOM MIN HEAP + OUTLIER DETECTION ----------
class MinHeap:
    def __init__(self):
        self.data = []

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i): return 2 * i + 1
    def _right(self, i): return 2 * i + 2

    def push(self, val):
        self.data.append(val)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        return self.data[0] if self.data else None

    def __len__(self):
        return len(self.data)

    def _sift_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self.data[p][0] <= self.data[i][0]:
                break
            self.data[p], self.data[i] = self.data[i], self.data[p]
            i = p

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            l = self._left(i)
            r = self._right(i)
            smallest = i
            if l < n and self.data[l][0] < self.data[smallest][0]:
                smallest = l
            if r < n and self.data[r][0] < self.data[smallest][0]:
                smallest = r
            if smallest == i:
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest


def compute_mean_std(values):
    n = len(values)
    if n == 0:
        return None, None
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    return mean, math.sqrt(variance)


def detect_fare_outliers():
    conn = sqlite3.connect("nyc_taxi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, fare_per_km FROM trips")
    rows = cursor.fetchall()
    conn.close()

    values = [r[1] for r in rows if r[1] is not None]
    mean, std = compute_mean_std(values)
    threshold_high = mean + 3 * std
    threshold_low = mean - 3 * std

    outliers = [r for r in rows if r[1] > threshold_high or r[1] < threshold_low]

    print("Outlier Trips Detected (by fare_per_km):")
    for o in outliers:
        print(f"Trip ID: {o[0]}, Fare/km: {o[1]:.2f}")
    print("Outlier detection complete.")


# ---------- MAIN ----------
if __name__ == "__main__":
    create_database()
    insert_sample_data()
    detect_fare_outliers()
