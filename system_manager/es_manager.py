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

    def retrive_entity_db_path(self):
        return self.entity_path

    def create_empty_entity_structure(self, _type="", _name=""):
        enum = AttributeType.resolve_type_from_str(_type)
        if enum == AttributeType.BEHAVIOR:
            return BehavioralEntity(_name)
        elif enum == AttributeType.STRUCTURAL:
            return StructuralEntity(_name)
        else:
            return None

    def create_system(self, entity:Entity):
        self.root_entity = entity

    def export_system_entity_structure(self, path=".", name="ses.json"):
        entity_data = OrderedDict()
        entity_data["name"] = self.root_entity.get_name()
        entity_data["type"] = self.root_entity.get_type()
        entity_data["attributes"] = self.root_entity.serialize_core_attribute()

        f = open(os.path.join(path, name), "w")
        f.write(json.dumps(entity_data, ensure_ascii=False, indent="\t"))
        f.close()
        #print(json.dumps(entity_data, ensure_ascii=False, indent="\t"))

    def export_system_entity_structure_recursively(self, path="."):
        entity_data = OrderedDict()
        entity_data["name"] = self.root_entity.get_name()
        entity_data["attributes"] = self.root_entity.attribute_to_list()
        #print(json.dumps(entity_data, ensure_ascii=False, indent="\t"))

    def import_system_entity_structure(self, path=".", name="ses.json"):

        json_data = open(os.path.join(path, name)).read()
        data = json.loads(json_data)
        name = data["name"]
        entity_type = data["type"]
        attributes = data["attributes"]

        self.root_entity = self.create_empty_entity_structure(entity_type, name)
        self.root_entity.deserialize_core_attribute(attributes)

        pass