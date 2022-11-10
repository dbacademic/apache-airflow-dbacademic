from datetime import datetime


from hello_operator import HelloOperator
from airflow.models import DAG

with DAG(
    dag_id='testa_plugin',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False,
    tags=['exemplo']
) as dag:
    hello_task = HelloOperator(task_id="sample-task", name="foo_bar")

hello_task