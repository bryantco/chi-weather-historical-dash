import openmeteo_requests
import polars as pl
import pandas
from datetime import datetime, timedelta, date
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

start_date = '2000-01-01'
end_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Request data -------------------------------------------------------------------------------------
# Request from Open-Meteo API ----
openmeteo = openmeteo_requests.Client()

url = "https://archive-api.open-meteo.com/v1/archive"
daily_vars = [
    "temperature_2m_mean", 
    "temperature_2m_max", 
    "temperature_2m_min", 
    "rain_sum", 
    "snowfall_sum", 
    "weather_code",
    "wind_speed_10m_mean", 
    "cloud_cover_mean",
    "relative_humidity_2m_mean"
]
params = {
    # Lat and lon for O'Hare
	"latitude": 41.978611,
	"longitude": -87.904724,
	"start_date": start_date,
	"end_date": end_date,
	"daily": daily_vars,
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
daily_wind_speed_10m_mean = daily.Variables(6).ValuesAsNumpy()
daily_cloud_cover_mean = daily.Variables(7).ValuesAsNumpy()
daily_relative_humidity_2m_mean = daily.Variables(8).ValuesAsNumpy()

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
daily_data["wind_speed_10m_mean"] = daily_wind_speed_10m_mean
daily_data["cloud_cover_mean"] = daily_cloud_cover_mean
daily_data["relative_humidity_2m_mean"] = daily_relative_humidity_2m_mean

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

# Write to the table
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres")

chi_weather_daily_df_pd = chi_weather_daily_df.to_pandas()
chi_weather_daily_df_pd.to_sql(name='chi_weather_daily', con=engine, if_exists='replace', index=False)


engine = create_engine(os.getenv('DATABASE_URL'))
chi_weather_daily_df_pd.to_sql(
    name='chi_weather_daily', 
    con=engine, 
    if_exists='replace', 
    index=False
)

print("Successfully wrote to the chi_weather_daily table.")


