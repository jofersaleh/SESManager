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

    @staticmethod
    def static_import_system_entity_structure(_path):
        ''' Temporarily '''
        json_data = open(_path).read()
        data = json.loads(json_data)
        name = data["name"]
        entity = EntityManager.create_entity_structure(name)

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

    def YN_Choice_menu(self, text):
        while True:
            opt = input(text + "(y/n)")
            if opt == "y":
                Flag = True
                return Flag
            elif opt == "n":
                Flag = False
                return Flag
            else:
                print("Please type only y or n")

    def Chk_int(self, _num):
        try:
            int(_num)
            return True
        except ValueError:
            print("please type int")
            return False

    @staticmethod
    def crud_menu():
        print("1. Create new Entity")
        print("2. Read Entity")
        print("3. Update Entity")
        print("4. Delete Entity")
        print("0. Exit")
        return int(input(">>"))

    def create_operation(self):
        esm = EntityManager()
        msa = ModelStructuralAttribute()
        entity = esm.create_entity_structure()
        list_entity_nm = []

        #setting name
        nm = input("Type name of Entity:")
        entity.set_name(nm)
        #setting input output
        Flag = True
        while Flag:
            inptnum = input("How many input port did system need")
            if self.Chk_int(inptnum):
                inptnum = int(inptnum)
                if inptnum == 0:
                    break
                for i in range(inptnum-1):
                        instnm = "in"+str(i+1)
                        msa.insert_input_port(instnm)
                Flag = False
        Flag = True
        while Flag:
            outptnum = input("How many output port did system need")
            if self.Chk_int(outptnum):
                outptnum = int(outptnum)
                if outptnum == 0:
                    break
                for i in range(outptnum-1):
                    outstnm = "out"+str(i+1)
                    msa.insert_output_port(outstnm)
                Flag = False
        #setting entity
        Flag = True
        while Flag:
            ntnm = input("What is the entity name?")
            list_entity_nm.append(ntnm)
            loop=True
            while loop:
                arti = input("Type number of arity")
                if self.Chk_int(arti):
                    arti = int(arti)
                    loop = False
            loop = True
            opt = 0
            while loop:
                opt = input("is this entity optional? (y/n)")
                if opt == "y":
                    opt = True
                    loop = False
                elif opt == "n":
                    opt = False
                    loop = False
                else:
                    print("Please type only y or n")
            msa.insert_entity(ntnm, arti, opt)
            Flag = self.YN_Choice_menu("Did you need more entity?")
        #setting coupling
        ask = self.YN_Choice_menu("Did you want to make input port?")
        if ask == True:
            Flag = True
            i = 0
            while Flag:
                print(list_entity_nm)
                input_entity = input("choose entity to connect with input port")
                if input_entity in list_entity_nm:
                    input_port = "in" + str(i)
                    msa.insert_coupling(("", input_port), (input_entity, "in"))
                    Flag = self.YN_Choice_menu("did you need more connection?")
                    if Flag == True:
                        i += 1
                        if inptnum < i:
                            print("no more port remain")
                            Flag = False
                else:
                    print("Not in a list. Please type again")
        ask = self.YN_Choice_menu("Did you want to make output port?")
        if ask == True:
            Flag = True
            i = 0
            while Flag:
                print(list_entity_nm)
                output_entity = input("choose entity to connect with output port")
                if output_entity in list_entity_nm:
                    output_port = "out" + str(i)
                    msa.insert_coupling((output_entity, output_port), ("", "out"))
                    Flag = self.YN_Choice_menu("did you need more connection?")
                    if Flag == True:
                        i += 1
                        if inptnum < i:
                            print("no more port remain")
                            Flag = False
                else:
                    print("Not in a list. Please type again")
        ask = self.YN_Choice_menu("Did you want to make internal port?")
        if ask == True:
            Flag = True
            while Flag:
                print(list_entity_nm)
                interaction_entity1 = input("choose first entity out to other")
                interaction_entity2 = input("choose second entity in by other")
                if (interaction_entity1 in list_entity_nm) & (interaction_entity2 in list_entity_nm):
                    msa.insert_coupling((interaction_entity1, "out"), (interaction_entity2, "in"))
                    Flag = self.YN_Choice_menu("did you need more connection?")
                else:
                    print("Not in a list. Please type again")


        entity.set_core_attribute(msa)
        esm.create_system(entity)
        esm.export_system_entity_structure(entity, self.entity_path, nm+".json")



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
        # TODO implement

        self.list_up_entity()
        selected = input("Select Entity to update:")
        if selected not in self.model_db:
            print("[ERR] Entity Not Found")
            pass
        model = self.import_system_entity_structure(self.model_db[selected])
        print(model)

        ###make menu to modify entities##

        print("What did you want to modify entity")
        print("1. Add Entity")
        print("2. delete Entity")
        print("3. modify Entity")
        print("0. Exit")

        # crteate new entities
        nmn = input("Type name of Entities to create:")



        json_data = open(self.model_db[selected]).read()
        data = json.loads(json_data)

        core = data["core_attribute"]
        if core["type"] == "STRUCTURAL":
            lst = core["entities"]
            lst.append([crte_enti])
        jsnlst = json.dumps(lst)
        print(jsnlst)
        core["entities"] = jsnlst
        data["core_attribute"] = core


        #modify original entities


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
