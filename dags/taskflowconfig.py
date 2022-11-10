import json
import requests

import types

import hashlib

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

from utils.source_config import sources

from simpot import graph



from rdflib import Namespace, Literal, URIRef
from simpot import RdfsClass, BNamespace
from rdflib.namespace import DC, FOAF


def serialize_to_rdf (data, type_class ):
    rdf = list( map(lambda d: type_class (d), data ) )
    return (graph(rdf)).serialize()

VCARD = Namespace('https://www.w3.org/2006/vcard/ns#')
DBO = Namespace('http://dbpedia.org/ontology/')
DC = Namespace('http://purl.org/dc/terms/#')
VIVO = Namespace("http://vivoweb.org/ontology/core#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
OWL = Namespace("http://www.w3.org/TR/owl-ref/")
OPENCIN = Namespace("http://purl.org/ontology/opencin/")
DBACAD = Namespace("http://purl.org/ontology/dbacademic/")
AIISO = Namespace("http://purl.org/vocab/aiiso/schema#")


ORG = Namespace ("https://www.w3.org/TR/vocab-org/")


OPENUAI = Namespace("http://purl.org/ontology/openuai#")


class Discente ():

    nome = FOAF.name
    curso = OPENCIN.isMemberOf
    code= DC.identifier

    university = ORG.memberOf

    @RdfsClass(OPENCIN.Student, "https://www.dbacademic.tech/resource/")
    @BNamespace('foaf', FOAF)
    @BNamespace('cin', OPENCIN)
    @BNamespace('aiiso', AIISO)
    @BNamespace('dc', DC)
    @BNamespace('dbacad', DBACAD)
    def __init__(self, dict ):
        self.nome = Literal(dict["nome"])
        self.id = dict["id"]
        self.code = dict["code"]
        if "curso" in dict:
            self.curso = URIRef(dict["curso"])
        if "university" in dict:
            self.university = URIRef(dict["university"])

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

        return serialize_to_rdf(total_order_value, Discente)

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary)
tutorial_etl_dag_2 = tutorial_taskflow_exemplo()


