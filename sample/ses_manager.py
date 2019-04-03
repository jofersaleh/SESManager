from system_manager.es_manager import EntityManager

esm = EntityManager()

entity = esm.create_empty_entity_structure("STRUCTURAL")
entity.set_name("System")
entity.insert_input_port("in1")
entity.insert_input_port("in2")

entity.insert_output_port("out1")
entity.insert_output_port("out2")

entity.insert_entity("en")
entity.insert_entity("en1")
entity.insert_coupling(("", "in1"), ("en", "in"))
entity.insert_coupling(("en", "out"), ("en1", "in"))
entity.insert_coupling(("en1", "out"), ("", "out"))

esm.create_system(entity)

esm.export_system_entity_structure("./sample/")
esm.import_system_entity_structure("./sample/")
esm.export_system_entity_structure("./sample/", "ses2.json")