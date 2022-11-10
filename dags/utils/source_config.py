import hashlib
import requests

from utils.models import Discente


def dados_ckan (url):
    data = requests.get(url+"&limit=5", verify=False).json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]



## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()


mapper_params = {

"discente_ufrn" :{
                    "nome" : "nome_discente",
                    "id": lambda d: hashcode ("ufrn", "discente", d["matricula"]),
                    "code" : "matricula",
                    "university" : lambda d: "http://dbpedia.org/resource/Federal_University_of_Rio_Grande_do_Norte",
                    "curso": lambda d: "https://www.dbacademic.tech/resource/" +  hashcode ( "ufrn", "curso", str (d["id_curso"]))
     },

 "discente_ufpa" :   {
                    "nome" : "Nome", 
                    "id": lambda d: hashcode ("ifpa", "discente", d["Matricula"]),
                    "university" : lambda d: "http://pt.dbpedia.org/resource/Instituto_Federal_do_Pará",
                    "code" : "Matricula",
                    #"curso": lambda d: "https://www.dbacademic.tech/resource/" + hashcode ( "ufma", "curso", str (d["codigo_curso"]))
            }

}

model_params = {
  "discente" : Discente
}

source_params = {
  "discente_ufrn" : "http://dados.ufrn.br/api/action/datastore_search?resource_id=a55aef81-e094-4267-8643-f283524e3dd7",
  "discente_ufpa" : "https://pda.ifpa.edu.br/api/action/datastore_search?resource_id=d422ed80-e077-492f-82dd-5827390b261f",
}

request_params = {
  "ckan" : dados_ckan
}



            



