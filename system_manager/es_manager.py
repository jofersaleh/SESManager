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
            self.model_db[_file[:-5]] = os.path.join(os.path.abspath(self.entity_path), _file)
        #print(self.model_db)

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

    def import_system_entity_structure(self, path, name):
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

    def import_system_entity_structure(self, _path):
        json_data = open(_path).read()
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

    def select_root_entity(self, _name):
        """
            Load selected root entity
            :param: _name: name of root entity
            :return:
        """
        if _name in self.model_db:
            self.import_system_entity_structure(self.model_db[_name])
        else:
            print("[ERR] Model not found")
        pass

    def list_up_entity(self):
        """
            Update file_db again and list up all entities
            :param: None
            :return:
        """
        self.file_db_init()
        fmt = "{0: <13}\t{1: <13}"
        print(fmt.format("Entity Name", "Path"))
        [print(fmt.format(k, v)) for k, v in self.model_db.items()]

    def interactive_pruning(self):
        self.list_up_entity()
        selected = input("Select Entity:")

        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
        else:
            self.import_system_entity_structure(self.model_db[selected])
            if self.root_entity:
                print("!")
                pass
            else:
                pass

    @staticmethod
    def crud_menu():
        print("1. Create new Entity")
        print("2. Read Entity")
        print("3. Update Entity")
        print("4. Delete Entity")
        print("0. Exit")
        return int(input(">>"))

    def create_operation(self):
        # TODO implement
        pass

    def read_operation(self):
        self.list_up_entity()
        selected = input("Select Entity:")

        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
        else:
            print(self)
        pass

    def update_operation(self):
        self.list_up_entity()
        # TODO implement
        pass

    def delete_operation(self):
        self.list_up_entity()
        selected = input("Select Entity:")

        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
        else:
            os.remove(self.model_db[selected])
            del(self.model_db[selected])
            print("Entity {} deleted".format(selected))
            self.list_up_entity()
        pass

    def start(self):
        loop = True
        while loop:
            selected = EntityManager.crud_menu()

            if selected == 1:
                pass
            elif selected == 2:
                self.read_operation()
                pass
            elif selected == 3:
                self.update_operation()
                pass
            elif selected == 4:
                self.delete_operation()
                pass
            else:
                loop = False
                pass
