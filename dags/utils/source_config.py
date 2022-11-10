import hashlib

## utils
def hashcode (university, resource,  code):
  return hashlib.md5((university+resource+code).encode()).hexdigest()

UFRN="http://dbpedia.org/resource/Federal_University_of_Rio_Grande_do_Norte"






sources = [

 {
     "url" : "http://dados.ufrn.br/api/action/datastore_search?resource_id=a55aef81-e094-4267-8643-f283524e3dd7",
     "mapper" :  {
                    "nome" : "nome_discente",
                    "id": lambda d: hashcode ("ufrn", "discente", d["matricula"]),
                    "code" : "matricula",
                    "university" : lambda d: UFRN,
                    "curso": lambda d: "https://www.dbacademic.tech/resource/" +  hashcode ( "ufrn", "curso", str (d["id_curso"]))
     }

  }
 
 ]


