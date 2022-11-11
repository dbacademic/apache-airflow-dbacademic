import json
import requests

import types

import hashlib

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

from utils.source_config import model_params, request_params, source_params

from simpot import mapper_all

from airflow.operators.python import task, get_current_context

from simpot import serialize_to_rdf



default_args = {
    'owner': 'airflow',
}

default_params = {
    "source" : "discente_ufrn",
    "model" : "discente",
    "request" : "ckan"
}

@dag(params=default_params, default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['exemplo'])
def exemplo_dbacademic_pipeline():

    @task()
    def extract():
        source_key = get_current_context()["params"]["source"]
        url = source_params[source_key]["url"]
        request_key = get_current_context()["params"]["request"]
        request_function = request_params[request_key]
        return request_function(url) # retornas apenas os dados, lista de json
        
    @task(multiple_outputs=False)
    def transform_json(data: [dict]):
        source_key = get_current_context()["params"]["source"]
        mapper = source_params[source_key]["mapper"]
        return list(mapper_all(mapper, data))



    @task()
    def transform_to_rdf(data: dict):
        model_key = get_current_context()["params"]["model"]
        model = model_params[model_key]
        return serialize_to_rdf(data, model)
        
        
    data = extract()
    data_json = transform_json(data)
    transform_to_rdf(data_json)

exemplo_dbacademic_pipeline()


