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

    @staticmethod
    def export_system_entity_structure(_entity, _path=".", name="ses.json"):
        entity_data = OrderedDict()
        entity_data["name"] = _entity.get_name()
        entity_data["core_attribute"] = _entity.serialize_core_attribute()

        f = open(os.path.join(_path, name), "w")
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
        entity = self.create_entity_structure(name)

        core = data["core_attribute"]
        if core["type"] == "STRUCTURAL":
            attr = ModelStructuralAttribute()
            attr.deserialize(core)
            entity.set_core_attribute(attr)
            return entity

        return None

    def import_system_entity_structure(self, _path):
        json_data = open(_path).read()
        data = json.loads(json_data)
        name = data["name"]
        entity = self.create_entity_structure(name)

        core = data["core_attribute"]
        if core["type"] == "STRUCTURAL":
            attr = ModelStructuralAttribute()
            attr.deserialize(core)
            entity.set_core_attribute(attr)
            return entity

        return None

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
            self.root_entity = self.import_system_entity_structure(self.model_db[selected])
            pes = self.root_entity.clone()
            pes.set_name("pruned_" + pes.get_name())

            entity_list = pes.check_validity()
            fmt = "{name: <10}\t{arity: <5}\t{opt: <5}"
            while entity_list:
                print("List of entities to pruning")
                for entity in entity_list:
                    print(fmt.format(name=entity[0], arity=entity[1], opt=entity[2]))
                choice = input("> Select entity to prune: ")

                if True in list(map(lambda x: x[0] == choice, entity_list)):
                    pes.prune(choice)
                else:
                    print("[ERR] Entity {} not found".format(choice))
                entity_list = pes.check_validity()
            print(">>> Pruned Entity Structure <<< ")
            print(pes)
            print("Stored in pes_db")
            pes_path = os.path.join(os.path.dirname(self.entity_path), "pes_db")

            self.export_system_entity_structure(pes, pes_path, pes.get_name() + ".json")

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
        self.list_up_entity()
        selected = input("Select Entity to create:")
        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
            pass

        nmn = input("Type name of Entity:")
        arti = int(input("Type number of arity"))
        A = True
        opt = 0
        while A:
            opt = input("is this entity optional? (y/n)")
            if opt == "y":
                opt = True
                A = False
            elif opt == "n":
                opt = False
                A = False
            else:
                print("Please type only y or n")
        print(nmn, arti, opt)
        crte_enti = [nmn, arti, opt]
        json_data = open(self.model_db[selected]).read()
        data = json.loads(json_data)

        core = data["core_attribute"]
        if core["type"] == "STRUCTURAL":
            lst = core["entities"]
            lst.append([crte_enti])
        print(lst)

        #print(self.model_db)
        #print(nmn)
        pass

    def read_operation(self):
        self.list_up_entity()
        selected = input("Select Entity:")

        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
        else:
            model = self.import_system_entity_structure(self.model_db[selected])
            print(model)
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
                self.create_operation()
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
