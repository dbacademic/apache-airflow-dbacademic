from datetime import datetime


from hello_operator import HelloOperator
from mapper_operator import MapperOperator
from airflow.models import DAG

with DAG(
    dag_id='testa_plugin',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False,
    tags=['exemplo']
) as dag:
    hello_task = HelloOperator(task_id="sample-task", name="foo_bar")

    config_task = MapperOperator(
        task_id="task_id_1",
        configuration={"query": {"job_id": "123", "sql": "select * from my_table"}},
        dag=dag,
    )

config_task >> hello_task