from model_base.behavior_model import BehaviorModel
from model_base.modelmanager import ModelManager
from system_manager.es_manager import EntityManager
from system_entity.structure_attribute import *
from system_manager.system_manager import *

esm = EntityManager("./sample/ses_db")

entity = esm.create_entity_structure()
entity.set_name("System")

msa = ModelStructuralAttribute()
msa.insert_input_port("in1")
msa.insert_input_port("in2")

msa.insert_output_port("out1")
msa.insert_output_port("out2")

msa.insert_entity("en", "*", True)
msa.insert_entity("en1", 2, True)
msa.insert_coupling(("", "in1"), ("en", "in"))
msa.insert_coupling(("en", "out"), ("en1", "in"))
msa.insert_coupling(("en1", "out"), ("", "out"))

entity.set_core_attribute(msa)
esm.create_system(entity)

esm.export_system_entity_structure(entity, "./sample/ses_db")

msa = BehaviorModel("en2")

msa.insert_state("Idle")
msa.insert_state("move", 1)

msa.insert_input_port("in1")
msa.insert_input_port("in2")

msa.insert_output_port("out1")
msa.insert_output_port("out2")

msa.insert_external_transition("idle", "in1", "move")
msa.insert_external_transition("move", "in2", "idle")

msa.insert_internal_transition("move", "out1", "idle")

mm = ModelManager("./sample/model_db")
mm.export_model(msa, "en2.json")

# esm.interactive_pruning()

sm = SystemManager("./sample/ses_db", "./sample/model_db")
sm.start()
