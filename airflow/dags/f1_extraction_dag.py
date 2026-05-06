from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Schedule to run every Monday at 12:00 PM (noon)
with DAG(
    'f1_race_extraction_dag',
    default_args=default_args,
    description='A simple DAG to extract F1 race results every Monday',
    schedule='0 12 * * 1',
    catchup=False,
    tags=['f1', 'extraction'],
) as dag:

    # Task to run the Python extraction script explicitly using the Airflow virtual environment
    # The script is mounted at /opt/airflow/etl/extract_race_results.py
    extract_task = BashOperator(
        task_id='extract_fastf1_data',
        bash_command='/opt/airflow-venv/bin/python /opt/airflow/etl/extract_race_results.py',
    )

    extract_task
