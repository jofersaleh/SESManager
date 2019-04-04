import sys
from system_entity.entity import *
from system_entity.attribute import *

import json
import os
from collections import OrderedDict


class EntityManager(object):
    def __init__(self):
        self.entity_path = ""
        self.root_entity = None

    def set_entity_db_path(self, path):
        self.entity_path = path

    def retrieve_entity_db_path(self):
        return self.entity_path

    @staticmethod
    def create_entity_structure(_name="None"):
        return Entity(_name)

    def create_system(self, entity: Entity):
        self.root_entity = entity

    def export_system_entity_structure(self, path=".", name="ses.json"):
        entity_data = OrderedDict()
        entity_data["name"] = self.root_entity.get_name()
        entity_data["core_attribute"] = self.root_entity.serialize_core_attribute()

        f = open(os.path.join(path, name), "w")
        f.write(json.dumps(entity_data, ensure_ascii=False, indent="\t"))
        f.close()

    def export_system_entity_structure_recursively(self, path="."):
        entity_data = OrderedDict()
        entity_data["name"] = self.root_entity.get_name()
        entity_data["core_attribute"] = self.root_entity.attribute_to_list()

    def import_system_entity_structure(self, path=".", name="ses.json"):
        json_data = open(os.path.join(path, name)).read()
        data = json.loads(json_data)
        name = data["name"]
        self.root_entity = self.create_entity_structure(name)

        core = data["core_attribute"]
        if core["type"] == "STRUCTURAL":
            attr = ModelStructuralAttribute()
            attr.deserialize(core)
            self.root_entity.set_core_attribute(attr)
        elif core["type"] == "BEHAVIOR":
            attr = ModelBehaviorAttribute()
            attr.deserialize(core)
            self.root_entity.set_core_attribute(attr)
            pass
