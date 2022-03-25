# Starlink Lookup
# Motivation
### Create a program that:
- Import the SpaceX Satellite data as a time series into a database
  - Json inside project/data
- Query the data to determine the last known latitude/longitude of the satellite for a given time
- Fetch from the database the closest satellite at a given time T, and a given a position on a globe as a (latitude, longitude) coordinate.
  - Using Haversine Formula

## Questions to the interviewer (Like we are working together)
- About the data 
  - Who is consuming the data and their needs?
    - Is important to understand how this CLI is helping the user solve the problem.
    - Like, the user will be using everyday? Every hour?
    - Can I import all the data in the morning once per day?
  - Volume?
  - File size?
  - Is useful to store with null values in Lat or Long?

- Design Choices
  - Memory over performance in reading the data.
    - Using ijson instead o Pandas, ijson have a Peak Memory usage of 8.0 MiB vs 265 MiB in Pandas (For a 35 MB json File)
    - With more info about the data (questions above) I can choose the better solution.
  - Filtering Null values.
    - The goal is to "determine the last known latitude/longitude of the satellite". Data without lat/long is not useful.
    - Less data to store.

## Requirements
- docker
- python >= 3.7

## Structure
```
├── project
│   ├── data
│   │   ├── starlink_historical_data.json
│   │   ├── starlink_historical_data_long.json
│   │   └── starlink_historical_data_small.json
│   ├── __init__.py
│   ├── main.py
│   ├── parsing
│   │   ├── __init__.py
│   │   ├── parsing.py
│   └── sql
│       ├── database.py
│       └── sat_query.py
├── README.md
└── requirements.txt
```

## How to run project locally
```
docker run -d -p 5432:5432 --name starlink -e POSTGRES_PASSWORD=blueonion -d postgres:13.6

git clone https://github.com/stifferdoroskevich/bol_challenge_starlink
cd bol_challenge_starlink
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd project
```

### Initialize DB
```
python main.py init-db
```
### Import data (json). In folder "project/data"
```
python main.py import-json
```

### Query
- Get Last Postion.
  - Parameter:
    - satellite_id (str)
```
python sql/sat_query.py get-last-position --satellite_id='60106f1fe900d60006e32c7f'
```

- Get Closest Satellite.
  - Parameters:
    - given_time (str) 
    - latitude (float)
    - longitude (float)
```
python sql/sat_query.py get-closest-satellite --given_time='2021-01-26T06:26:10' --latitude=-25.4813585 --longitude=-54.7656224
```

### To Delete All Rows
```
python main.py delete-all-rows
```
