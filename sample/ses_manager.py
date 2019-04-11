from system_manager.es_manager import EntityManager
from system_entity.structure_attribute import *

esm = EntityManager("./sample/db")

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

esm.export_system_entity_structure("./sample/db")
esm.import_system_entity_structure("./sample/db")
esm.export_system_entity_structure("./sample/db", "ses2.json")