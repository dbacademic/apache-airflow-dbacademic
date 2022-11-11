import hashlib
import requests

from utils.models import Discente, Curso


def dados_ckan (url):
    data = requests.get(url+"&limit=5", verify=False).json()
    print (len (data["result"]["records"] ))
    return data["result"]["records"]

def dados_ufma (url):
    data = requests.get(url).json()
    return data["data"]

## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()

IFRN="http://pt.dbpedia.org/resource/Instituto_Federal_do_Rio_Grande_do_Norte"
IFMA="http://pt.dbpedia.org/resource/Instituto_Federal_do_Maranhão"
IFPA="http://pt.dbpedia.org/resource/Instituto_Federal_do_Pará"
UFRN="http://pt.dbpedia.org/resource/Universidade_Federal_do_Rio_Grande_do_Norte"
IFS="http://pt.dbpedia.org/resource/Instituto_Federal_de_Sergipe"
IFMS="http://pt.dbpedia.org/resource/Instituto_Federal_de_Mato_Grosso_do_Sul"
UFCSPA="http://pt.dbpedia.org/resource/Universidade_Federal_de_Ciências_da_Saúde_de_Porto_Alegre"
UFV="http://pt.dbpedia.org/resource/Universidade_Federal_de_Viçosa"
UFCA="http://pt.dbpedia.org/resource/Universidade_Federal_do_Cariri"
UFPI="http://pt.dbpedia.org/resource/Universidade_Federal_do_Piauí"
UFSJ="http://pt.dbpedia.org/resource/Universidade_Federal_de_S%C3%A3o_Jo%C3%A3o_del-Rei"
IFPB="http://pt.dbpedia.org/resource/Instituto_Federal_da_Paraíba"
UNIRIO="http://pt.dbpedia.org/resource/Universidade_Federal_do_Estado_do_Rio_de_Janeiro"
UFFS="http://pt.dbpedia.org/resource/Universidade_Federal_da_Fronteira_Sul"
UFPB="http://pt.dbpedia.org/resource/Universidade_Federal_do_Paraíba"
UNIFESSPA="http://pt.dbpedia.org/resource/Universidade_Federal_do_Sul_e_Sudeste_do_Pará"
UFMA="http://pt.dbpedia.org/resource/Universidade_Federal_do_Maranhão"
UFPEL="http://pt.dbpedia.org/resource/Universidade_Federal_de_Pelotas"
IFFAR="http://pt.dbpedia.org/resource/Instituto_Federal_Farroupilha"
UFMS="http://pt.dbpedia.org/resource/Universidade_Federal_do_Mato_Grosso_do_Sul"
UFOP="http://pt.dbpedia.org/resource/Universidade_Federal_de_Ouro_Preto"
IFC="http://pt.dbpedia.org/resource/Instituto_Federal_Catarinense"
UFERSA="http://pt.dbpedia.org/resource/Universidade_Federal_Rural_do_Semi-Árido"
IFPI="http://pt.dbpedia.org/resource/Instituto_Federal_do_Piauí"
UFOB="http://pt.dbpedia.org/resource/Universidade_Federal_do_Oeste_da_Bahia"


mapper_params = {

"discente_ufrn" :{
                    "nome" : "nome_discente",
                    "id": lambda d: hashcode ("ufrn", "discente", d["matricula"]),
                    "code" : "matricula",
                    "university" : lambda d: UFRN,
                    "curso": lambda d: "https://www.dbacademic.tech/resource/" +  hashcode ( "ufrn", "curso", str (d["id_curso"]))
     },

 "discente_ifpa" :   {
                    "nome" : "Nome", 
                    "id": lambda d: hashcode ("ifpa", "discente", d["Matricula"]),
                    "university" : lambda d: IFPA,
                    "code" : "Matricula",
                    #"curso": lambda d: "https://www.dbacademic.tech/resource/" + hashcode ( "ufma", "curso", str (d["codigo_curso"]))
            },

  "discente_ufma" : {
                    "nome" : "nome", 
                    "id": lambda d: hashcode ("ufma", "discente", d["matricula"]),
                    "code" : "matricula",
                    "university" : lambda d: UFMA,
                    "curso": lambda d: "https://www.dbacademic.tech/resource/" + hashcode ( "ufma", "curso", str (d["codigo_curso"]))
            },


    ## cursos

    "curso_ufms" : {
                    "nome" : "curso", 
                    "code" : "id",
                    "id": lambda d: hashcode ( "ufms",  "curso", str (d["id"])),
                    "university" : lambda d: UFMS,
                    
            } 

}

model_params = {
  "discente" : Discente,
  "curso" : Curso,
}

source_params = {
  "discente_ufrn" : "http://dados.ufrn.br/api/action/datastore_search?resource_id=a55aef81-e094-4267-8643-f283524e3dd7",
  "discente_ifpa" : "https://pda.ifpa.edu.br/api/action/datastore_search?resource_id=d422ed80-e077-492f-82dd-5827390b261f",
  "discente_ufma" : "https://dados-ufma.herokuapp.com/api/v01/discente/",

  #cursos
  "curso_ufms" : "https://dadosabertos.ufms.br/api/action/datastore_search?resource_id=e239fd31-fe43-45e1-9d84-ba60a8d7fae7",
}

request_params = {
  "ckan" : dados_ckan,
  "ufma"  : dados_ufma,
}



            



