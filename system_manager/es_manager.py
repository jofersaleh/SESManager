from system_entity.entity import *
# from model_base.behavior_model import *
from system_entity.structure_attribute import *

import json
import os
from collections import OrderedDict
from os import listdir
from os.path import isfile, join


class EntityManager(object):

    @staticmethod
    def create_entity_structure(_name="None"):
        return Entity(_name)

    def __init__(self, path="."):
        self.entity_path = path
        self.root_entity = None
        self.entity_db = []
        self.model_db = {} #defaultdict(list)
        self.file_db_init()

    def file_db_init(self):
        self.entity_db = [f for f in listdir(self.entity_path) if isfile(join(self.entity_path, f))]
        for _file in self.entity_db:
            self.model_db[_file[:-4]] = os.path.join(os.path.abspath(self.entity_path), _file)
        print(self.model_db)

    def set_entity_db_path(self, path):
        self.entity_path = path
        self.file_db_init()

    def retrieve_entity_db_path(self):
        return self.entity_path

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
        # elif core["type"] == "BEHAVIOR":
        #     attr = ModelBehaviorAttribute()
        #     attr.deserialize(core)
        #     self.root_entity.set_core_attribute(attr)
            pass

    def select_alternatives(self):
        pass

    def interactive_pruning(self):
        if self.root_entity :
            print("Root entity is not selected")
            pass
        else:
            pass