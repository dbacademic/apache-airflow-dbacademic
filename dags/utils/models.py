



from rdflib import Namespace, Literal, URIRef
from simpot import RdfsClass, BNamespace
from rdflib.namespace import DC, FOAF




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
