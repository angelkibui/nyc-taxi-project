# NYC Taxi Project

## Overview
The **NYC Taxi Project** is part of an enterprise-level fullstack data engineering assignment focused on analyzing urban mobility data from the **New York City Taxi Trip dataset**.  

---

## 1. Backend Project Structure
nyc-taxi-project/
- data;  ( yellow_tripdata_2025-08.parquet) # Raw dataset files
  processed data (cleaned_taxi_data.csv) # Cleaned dataset output
- src; clean_data.py # Main Python script for cleaning and processing
-  (`venv`) ; # Virtual environment
- requirements.txt # List of Python dependencies
- README.md # Project documentation 
- .gitignore # Files and folders ignored by Git
---

## 2. Setup Instructions

### Prerequisites
Before running the project, ensure you have:
- Python 3.8 or higher installed
- Virtual environment (`venv`) set up
- A CSV or Parquet version of the NYC Taxi dataset

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/angelkibui/nyc-taxi-project.git
   cd nyc-taxi-project
2. **create virtual environment**
   python -m venv venv
   source venv/bin/activate   
3. **install dependancies**
   pip install -r requirements.txt
4. **Download the Dataset**
  Due to GitHub file size limits, the raw NYC Taxi dataset is not included in this repository.

Go to the NYC TLC Trip Record Data Page

Download one month of data (e.g. yellow_tripdata_2025-08.parquet)

Place it in:

data/raw/

5. **run the script**
Once the dataset is downloaded and placed in the correct folder, run:

python src/clean_data.py


This script will:
Clean and format the data
Create new features
Remove invalid or missing records

Save the final output in:

data/processed/cleaned_taxi_data.csv

### output
After processing, the cleaned dataset includes features such as:

| pickup_datetime  | dropoff_datetime | trip_distance | trip_duration_min | fare_amount | trip_speed | fare_per_km |
| ---------------- | ---------------- | ------------- | ----------------- | ----------- | ---------- | ----------- |
| 2025-08-01 08:32 | 2025-08-01 08:51 | 5.2           | 19                | 17.5        | 16.4       | 3.36        |

## Note
The raw and cleaned files are too large to upload to GitHub (over 100 MB).
To keep the project runnable:

Only the code and structure are included.



