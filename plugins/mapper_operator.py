

from airflow.models.baseoperator import BaseOperator


def dados_ckan (url):
    data = requests.get(url+"&limit=5").json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]


def mapper_item (data, value):
    if isinstance(value, types.FunctionType):
        return value (data)
    if isinstance(value, str):
        return data[value]

def mapper_one (mapper, data ):
    return {item : mapper_item (data, value) for (item, value) in mapper.items()} 

def mapper_all (mapper, data):
    return list(map (lambda d: mapper_one(mapper, d), data  ))
       

class MapperOperator(BaseOperator):

    def __init__(self, configuration: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.configuration = configuration

    def execute(self, context):
        return self.configuration