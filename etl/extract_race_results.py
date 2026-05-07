import os
import fastf1
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (useful if running outside Docker)
load_dotenv(dotenv_path='../.env')

# Database configuration
# We use 'postgres' and 5432 because the devcontainer will join the compose network.
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('POSTGRES_ADMIN_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_ADMIN_PASSWORD', 'postgres')
DB_NAME = os.getenv('POSTGRES_ADMIN_DB', 'f1_warehouse')

# Enable FastF1 cache to speed up repeated requests
CACHE_DIR = './cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)


def extract_season_results(year: int):
    """Extracts enriched race results for an entire season."""
    print(f"Loading schedule for {year}...")
    schedule = fastf1.get_event_schedule(year)

    # Filter out testing events
    races = schedule[schedule['EventFormat'] != 'testing']

    all_results = []

    for _, race in races.iterrows():
        round_num = race['RoundNumber']
        race_name = race['EventName']

        print(f"Extracting Round {round_num}: {race_name}...")
        try:
            session = fastf1.get_session(year, round_num, 'R')
            # Load without telemetry for speed, but include weather and laps
            session.load(telemetry=False, weather=True, messages=False)

            # Skip if race hasn't happened yet (no results)
            if session.results is None or session.results.empty:
                print(f"No results for {race_name} yet. Skipping.")
                continue

            df = session.results.copy()

            # Determine if it was a wet race
            weather = session.weather_data
            is_wet = False
            if weather is not None and not weather.empty:
                is_wet = (weather['Rainfall'] > 0).any()

            # Calculate lap stats
            laps = session.laps
            lap_stats = pd.DataFrame()
            if laps is not None and not laps.empty:
                # Convert timedelta to seconds for easier averaging in SQL later
                laps['LapTime_sec'] = laps['LapTime'].dt.total_seconds()
                lap_stats = laps.groupby('DriverNumber').agg(
                    best_lap_time=('LapTime_sec', 'min'),
                    avg_lap_time=('LapTime_sec', 'mean')
                ).reset_index()

            if not lap_stats.empty:
                df = df.merge(lap_stats, on='DriverNumber', how='left')
            else:
                df['best_lap_time'] = None
                df['avg_lap_time'] = None

            # Keep relevant columns
            columns_to_keep = [
                'DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName',
                'Position', 'GridPosition', 'Points', 'Laps', 'Time', 'Status',
                'best_lap_time', 'avg_lap_time'
            ]
            # Time column can be tricky to insert to Postgres if it's timedelta. Let's cast to string.
            df['Time'] = df['Time'].astype(str)

            # Select columns (handling missing gracefully)
            df = df[[c for c in columns_to_keep if c in df.columns]]

            # Add metadata
            df['year'] = year
            df['round'] = round_num
            df['race_name'] = race_name
            df['is_wet_race'] = is_wet

            all_results.append(df)

        except Exception as e:
            print(f"Failed to extract {race_name}: {e}")

    if not all_results:
        return pd.DataFrame()

    return pd.concat(all_results, ignore_index=True)


def load_to_postgres(df: pd.DataFrame, table_name: str, schema: str = 'raw'):
    """Loads a Pandas DataFrame into the Postgres data warehouse."""
    print(f"Loading {len(df)} rows into {schema}.{table_name}...")

    # Create SQLAlchemy engine
    engine_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)

    # Instead of 'replace' (which drops the table without CASCADE and fails if views depend on it),
    # we drop with CASCADE so that Pandas can recreate it with new columns.
    with engine.connect() as conn:
        from sqlalchemy import text
        try:
            conn.execute(
                text(f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE;"))
            conn.commit()
        except Exception as e:
            print(f"Drop skipped: {e}")

    # Write to database
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists='append',
        index=False
    )
    print("Load complete!")


if __name__ == "__main__":
    # Extract data for the current/requested year
    target_year = 2026
    try:
        season_df = extract_season_results(target_year)

        if not season_df.empty:
            load_to_postgres(
                season_df, table_name='race_results', schema='raw')
        else:
            print("No data extracted.")
    except Exception as e:
        print(f"ETL Process failed: {e}")
