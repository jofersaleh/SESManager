from model_base.behavior_model import BehaviorModel
from model_base.modelmanager import ModelManager
from system_manager.es_manager import EntityManager
from system_entity.structure_attribute import *
from system_manager.system_manager import *

esm = EntityManager("./sample/ses_db")

entity = esm.create_entity_structure()
entity.set_name("Agent")

msa = ModelStructuralAttribute()
msa.insert_input_port("env")
msa.insert_input_port("agent")

msa.insert_output_port("env")
msa.insert_output_port("agent")

msa.insert_entity("sensors", 1, True)
msa.insert_entity("processor", 2, False)
msa.insert_entity("actuators", 1, False)

msa.insert_coupling(("", "env"), ("sensors", "env"))
msa.insert_coupling(("", "agent"), ("sensors", "agent"))

msa.insert_coupling(("sensors", "event"), ("process", "event"))
msa.insert_coupling(("processor", "control"), ("actuators", "control"))

msa.insert_coupling(("actuators", "out"), ("", "out"))

entity.set_core_attribute(msa)
# esm.create_system(entity)

esm.export_system_entity_structure(entity, "./sample/ses_db")
'''
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
'''
sm = SystemManager("./sample/ses_db", "./sample/model_db")
sm.start()

