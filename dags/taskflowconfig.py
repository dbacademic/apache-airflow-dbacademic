import json
import requests

import types

import hashlib

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

from utils.source_config import sources

def dados_ckan (url):
    data = requests.get(url+"&limit=5").json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]


## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()


def mapper_item (data, value):
    if isinstance(value, types.FunctionType):
        return value (data)
    if isinstance(value, str):
        return data[value]

def mapper_one (mapper, data ):
    return {item : mapper_item (data, value) for (item, value) in mapper.items()} 

def mapper_all (mapper, data):
    return list(map (lambda d: mapper_one(mapper, d), data  ))

UFRN="http://dbpedia.org/resource/Federal_University_of_Rio_Grande_do_Norte"



     
mapper = sources[0]["mapper"]
url = sources[0]["url"]

default_args = {
    'owner': 'airflow',
}


@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['exemplo'])
def tutorial_taskflow_exemplo():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple ETL data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/stable/tutorial_taskflow_api.html)
    """
    @task()
    def extract():
        return dados_ckan(url)
        
    @task(multiple_outputs=False)
    def transform(order_data_dict: [dict]):


        return mapper_all(mapper, order_data_dict)


    @task()
    def load(total_order_value: dict):
        """import types
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        print(total_order_value)
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary)
tutorial_etl_dag_2 = tutorial_taskflow_exemplo()


