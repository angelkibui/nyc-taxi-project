import pandas as pd

def clean_taxi_data():
    print("Loading raw taxi data...")
    df = pd.read_csv("data/raw/demo_small.csv")
    print("Loaded!", len(df), "rows")

    # Remove empty or invalid rows
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "fare_amount"])
    df = df[df["trip_distance"] > 0]
    df = df[df["fare_amount"] > 0]

    # Add new columns (derived features)
    df["trip_duration_min"] = (pd.to_datetime(df["tpep_dropoff_datetime"]) - pd.to_datetime(df["tpep_pickup_datetime"])).dt.total_seconds() / 60
    df["speed_kmh"] = (df["trip_distance"] / df["trip_duration_min"]) * 60
    df["fare_per_km"] = df["fare_amount"] / df["trip_distance"]

    # Save cleaned data
    df.to_csv("data/processed/cleaned_taxi_data.csv", index=False)
    print("Cleaned data saved to data/processed/cleaned_taxi_data.csv")

if __name__ == "__main__":
    clean_taxi_data()
