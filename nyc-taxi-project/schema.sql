-- schema.sql (SQLite)
PRAGMA foreign_keys = ON;

-- locations table to deduplicate coordinates
CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(latitude, longitude)
);

-- payment types dimension
CREATE TABLE IF NOT EXISTS payment_types (
    payment_type TEXT PRIMARY KEY,
    description TEXT
);

-- time dimension (optional) - stores unique datetimes
CREATE TABLE IF NOT EXISTS time_dim (
    time_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dt TEXT NOT NULL UNIQUE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    weekday INTEGER
);

-- trips fact table
CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_trip_id TEXT,
    pickup_location_id INTEGER NOT NULL,
    dropoff_location_id INTEGER NOT NULL,
    pickup_time_id INTEGER,
    dropoff_time_id INTEGER,
    pickup_datetime TEXT NOT NULL,
    dropoff_datetime TEXT NOT NULL,
    trip_duration_secs INTEGER NOT NULL,
    trip_distance_km REAL NOT NULL,
    fare_amount REAL NOT NULL,
    tip_amount REAL NOT NULL,
    passenger_count INTEGER,
    payment_type TEXT,
    avg_speed_kmph REAL,
    fare_per_km REAL,
    FOREIGN KEY (pickup_location_id) REFERENCES locations(location_id),
    FOREIGN KEY (dropoff_location_id) REFERENCES locations(location_id),
    FOREIGN KEY (pickup_time_id) REFERENCES time_dim(time_id),
    FOREIGN KEY (dropoff_time_id) REFERENCES time_dim(time_id),
    FOREIGN KEY (payment_type) REFERENCES payment_types(payment_type)
);

-- helpful indexes
CREATE INDEX IF NOT EXISTS idx_trips_pickup_dt ON trips(pickup_datetime);
CREATE INDEX IF NOT EXISTS idx_trips_dropoff_dt ON trips(dropoff_datetime);
CREATE INDEX IF NOT EXISTS idx_trips_pickup_loc ON trips(pickup_location_id);
CREATE INDEX IF NOT EXISTS idx_trips_avg_speed ON trips(avg_speed_kmph);
