from system_manager.es_manager import EntityManager
from model_base.behavior_model import *
from model_base.modelmanager import *
from system_entity.structure_attribute import *
from system_entity.runtime_attribute import *

esm = EntityManager()

entity = esm.create_entity_structure()
entity.set_name("System")

msa = ModelStructuralAttribute()
msa.insert_input_port("in1")
msa.insert_input_port("in2")

msa.insert_output_port("out1")
msa.insert_output_port("out2")

msa.insert_entity("en")
msa.insert_entity("en1")
msa.insert_coupling(("", "in1"), ("en", "in"))
msa.insert_coupling(("en", "out"), ("en1", "in"))
msa.insert_coupling(("en1", "out"), ("", "out"))

ra = RuntimeAttribute()
ra.insert_entity("en")
ra.insert_entity("en1")
ra.insert_model_path("en", "./sample/model_db/en.mi")
ra.insert_model_path("en1", "./sample/model_db/en1.mi")

ra.insert_domain_path("en", "./sample/domain_db/en.di")

entity.set_core_attribute(msa)
entity.insert_attribute(ra)

esm.create_system(entity)

esm.export_system_entity_structure(entity, "./", "test_structure.json")
entity = esm.import_system_entity_structure("./test_structure.json")
esm.export_system_entity_structure(entity, "./", "answer_structure.json")


def test_structure():
    f1 = open("./test_structure.json", "r")
    f2 = open("./answer_structure.json", "r")

    l1 = f1.readlines()
    l2 = f2.readlines()

    if len(l1) != len(l2):
        assert False

    for i in range(len(l1)):
        assert l1[i] == l2[i]

    # Test termination
    f1.close()
    f2.close()
    os.remove("./test_structure.json")
    os.remove("./answer_structure.json")