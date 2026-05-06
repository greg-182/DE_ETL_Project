import os
import fastf1
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (useful if running outside Docker)
load_dotenv(dotenv_path='../.env')

# Database configuration
# When running locally in Dev Container, we use localhost and the mapped port 5433.
# When running inside Airflow later, we will use 'postgres' and 5432.
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_USER = os.getenv('POSTGRES_ADMIN_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_ADMIN_PASSWORD', 'postgres')
DB_NAME = os.getenv('POSTGRES_ADMIN_DB', 'f1_warehouse')

# Enable FastF1 cache to speed up repeated requests
CACHE_DIR = './cache'
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def extract_race_results(year: int, race_name: str):
    """Extracts race results for a specific year and race."""
    print(f"Extracting race results for {year} {race_name}...")
    
    # Load the session (Race)
    session = fastf1.get_session(year, race_name, 'R')
    session.load()
    
    # Get the results as a Pandas DataFrame
    results = session.results
    
    # Select only the columns we care about to keep the raw data clean
    columns_to_keep = [
        'DriverNumber', 'BroadcastName', 'Abbreviation', 'TeamName',
        'Position', 'GridPosition', 'Points', 'Laps', 'Time', 'Status'
    ]
    df = results[columns_to_keep].copy()
    
    # Add metadata columns
    df['year'] = year
    df['race_name'] = race_name
    
    return df

def load_to_postgres(df: pd.DataFrame, table_name: str, schema: str = 'raw'):
    """Loads a Pandas DataFrame into the Postgres data warehouse."""
    print(f"Loading {len(df)} rows into {schema}.{table_name}...")
    
    # Create SQLAlchemy engine
    engine_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)
    
    # Write to database (replace if exists for this simple example)
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists='replace', # For production, we'd use 'append' and handle upserts
        index=False
    )
    print("Load complete!")

if __name__ == "__main__":
    # Example: Extract the 2023 Bahrain Grand Prix
    try:
        race_df = extract_race_results(2023, 'Bahrain')
        
        # Load into the 'raw' schema
        load_to_postgres(race_df, table_name='race_results', schema='raw')
        
    except Exception as e:
        print(f"ETL Process failed: {e}")
