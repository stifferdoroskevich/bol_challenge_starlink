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