import pytest
import os

from system_manager.es_manager import EntityManager
from system_entity.attribute import *

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

entity.set_core_attribute(msa)
esm.create_system(entity)

esm.export_system_entity_structure("./", "test.json")
esm.import_system_entity_structure("./", "test.json")
esm.export_system_entity_structure("./", "answer.json")


def test_structure():
    f1 = open("./test.json", "r")
    f2 = open("./answer.json", "r")

    l1 = f1.readlines()
    l2 = f2.readlines()

    if len(l1) != len(l2):
        assert False

    for i in range(len(l1)):
        assert l1[i] == l2[i]

    # Test termination
    f1.close()
    f2.close()
    os.remove("test.json")
    os.remove("answer.json")
