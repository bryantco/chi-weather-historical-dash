import openmeteo_requests
import requests_cache
from retry_requests import retry
import polars as pl
from datetime import datetime, timedelta, date
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

start_date = '2000-01-01'
end_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Request data -------------------------------------------------------------------------------------
# Request from Open-Meteo API ----
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    # Lat and lon for O'Hare
	"latitude": 41.978611,
	"longitude": -87.904724,
	"start_date": start_date,
	"end_date": end_date,
	"daily": ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "rain_sum", "snowfall_sum", "weather_code"],
	"timezone": "America/Chicago",
    'temperature_unit': 'fahrenheit',
    'wind_speed_unit': 'mph',
    'precipitation_unit': 'inch'
}

responses = openmeteo.weather_api(url, params=params)

# Process the response as daily data ----
response = responses[0]

daily = response.Daily()
daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_rain_sum = daily.Variables(3).ValuesAsNumpy()
daily_snowfall_sum = daily.Variables(4).ValuesAsNumpy()
daily_weather_code = daily.Variables(5).ValuesAsNumpy()

daily_data = {
	"date": pl.date_range(
        	start=datetime.strptime(start_date, '%Y-%m-%d').date(),
			end=datetime.strptime(end_date, '%Y-%m-%d').date(),
			interval=timedelta(days=1),
			closed='both',
			eager=True
	)
}

daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["rain_sum"] = daily_rain_sum
daily_data["snowfall_sum"] = daily_snowfall_sum
daily_data["weather_code"] = daily_weather_code

# Convert to polars df; one row per day, one column per weather metric
chi_weather_daily_df = pl.DataFrame(daily_data)

# Generate YMD features ----
chi_weather_daily_df = chi_weather_daily_df.with_columns(
    year=pl.col('date').dt.year(),
    month=pl.col('date').dt.month(),
    day=pl.col('date').dt.day()
).with_columns(
    month_day=pl.col('date').dt.strftime('%m-%d')
)

# Sync with Postgres -------------------------------------------------------------------------------
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = psycopg2.connect(
    dbname="postgres",
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

cur = conn.cursor()

# Write to the table
chi_weather_daily_df_pd = chi_weather_daily_df.to_pandas()
engine = create_engine(os.getenv('DATABASE_URL'))
chi_weather_daily_df_pd.to_sql('chi_weather_daily', engine, if_exists='replace', index=False)

print("Successfully wrote to the chi_weather_daily table.")

cur.close()
conn.close()

