from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="absenteismo_pipeline",
    description="Pipeline de dados de absenteismo: carga, transformacao e testes",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["absenteismo", "dbt", "portfolio"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test",
    )

    dbt_run >> dbt_test
