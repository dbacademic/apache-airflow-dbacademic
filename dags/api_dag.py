import json
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain


def save_posts(ti) -> None:
    posts = ti.xcom_pull(task_ids=['get_posts'])
    #print (posts)
    dados = (posts[0])
    #str =  dados # "".join(str(e) for e in dados)
    f = open("/opt/airflow/logs/demofile2.txt", "a")
    f.write(str(dados))
    f.close()


with DAG(
    dag_id='api_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 3, 1),
    catchup=False
) as dag:
    # 1. Check if the API is up
    task_get_posts = SimpleHttpOperator(
        task_id='get_posts',
        http_conn_id='api_post',
        #endpoint='/',
        method='GET',
        #response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    # 3. Save the posts
    task_save = PythonOperator(
        task_id='save_posts',
        python_callable=save_posts
    )

    chain(task_get_posts,task_save)
