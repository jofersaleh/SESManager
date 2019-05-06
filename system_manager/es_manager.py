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
        entity_data["core_attribute"] = _entity.get_core_attribute().serialize()
        entity_data["optional_attributes"] = _entity.serialize_attributes()
        f = open(os.path.join(_path, name), "w")
        f.write(json.dumps(entity_data, ensure_ascii=False, indent="\t"))
        f.close()

    '''    def import_system_entity_structure(self, path, name):
        json_data = open(os.path.join(path, name)).read()
        data = json.loads(json_data)
        name = data["name"]
        entity = self.create_entity_structure(name)

        core = data["core_attribute"]
        if core["type"] == "ASPECT":
            attr = ModelStructuralAttribute()
            attr.deserialize(core)
            entity.set_core_attribute(attr)
            return entity

        return None'''

    def import_system_entity_structure(self, _path):
        json_data = open(_path).read()
        data = json.loads(json_data)
        name = data["name"]
        entity = self.create_entity_structure(name)

        core = data["core_attribute"]

        attr = ModelStructuralAttribute()
        attr.deserialize(core)
        entity.set_core_attribute(attr)

        if "optional_attributes" in data:
            entity.deserialize_attributes(data["optional_attributes"])

        return entity


    @staticmethod
    def static_import_system_entity_structure(_path):
        ''' Temporarily '''
        json_data = open(_path).read()
        data = json.loads(json_data)
        name = data["name"]
        entity = EntityManager.create_entity_structure(name)

        core = data["core_attribute"]
        #if core["type"] == "ASPECT":
        attr = ModelStructuralAttribute()
        attr.deserialize(core)
        entity.set_core_attribute(attr)

        if "optional_attributes" in data:
            entity.deserialize_attributes(data["optional_attributes"])

        return entity

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

            # cbchoi added
            choice = input(">>> Do you want to synthesize executable? (y/N)")
            if choice == 'y':
                ra = RuntimeAttribute()
                entity_list = pes.get_core_attribute().retrieve_entities()
                for entity in entity_list:
                    choice = input(">>> Do you want to add model instance? (y/N)")
                    if choice == "y":
                        ra.insert_entity(entity[0])
                        mpath = input(">>> Enter path of {}'s model instance: ".format(entity[0]))
                        ra.insert_model_path(entity[0], mpath)
                        choice = input(">>> Do you want to add domain instance? (y/N)")
                        if choice == "y":
                            dpath = input(">>> Enter path of {}'s domain instance: ".format(entity[0]))
                            ra.insert_domain_path(entity[0], dpath)
                        pass
                    else:
                        continue
                    pass
                pes.insert_attribute(ra)

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
                for i in range(inptnum):
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
                for i in range(outptnum):
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
            i = 1
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
            i = 1
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
        esm = EntityManager()
        entity = esm.create_entity_structure()
        self.list_up_entity()
        while True:
            selected = input("Select Entity to update:")
            if selected not in self.model_db:
                print("[ERR] Entity Not Found")
            else:
                break
        #load datafile
        json_data = open(self.model_db[selected]).read()
        data = json.loads(json_data)
        aft_msa = ModelStructuralAttribute()
        entity.set_name(selected)
        core = data["core_attribute"]
        for ntnm, arti, opt in core["entities"]:
            aft_msa.insert_entity(ntnm, arti, opt)
        aft_msa.input_ports = core["input_ports"]
        aft_msa.output_ports = core["output_ports"]
        aft_msa.external_input_map = core["external_input"]
        aft_msa.external_output_map = core["external_output"]
        aft_msa.internal_coupling_map_entity = core["internal"]

        ###make menu to modify entities##
        loop = True
        while loop:
            print("What did you want to modify entity")
            print("1. Add Entity")
            print("2. Delete Entity")
            print("3. Modify Entity")
            print("4. Modify Port")
            print("0. Exit")
            _menu = input(">>")
            if self.Chk_int(_menu):
                _menu = int(_menu)
                if _menu == 1:
                    aft_msa = self.update_opt_addenti(aft_msa)
                    pass
                elif _menu == 2:
                    aft_msa = self.update_opt_deletenti(aft_msa)
                    pass
                elif _menu == 3:
                    aft_msa = self.update_opt_modienti(aft_msa, selected)
                    pass
                elif _menu == 4:
                    #aft_msa = self.update_opt_modiport(aft_msa)
                    self.update_opt_modiport(aft_msa)
                    pass
                elif _menu == 0:
                    loop = False
                else:
                    print("please type again")
            #update entity
            entity.set_core_attribute(aft_msa)
            esm.create_system(entity)
            esm.export_system_entity_structure(entity, self.entity_path, selected+".json")




    def update_opt_addenti(self, aft_msa):
        #1. adding entity
        modi_msa = ModelStructuralAttribute()
        Flag = True
        while Flag:
            ntnm = input("What is the entity name?")
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
            modi_msa.insert_entity(ntnm, arti, opt)
            Flag = self.YN_Choice_menu("Did you need more entity?")

        lst = []
        for addentiy in modi_msa.entity_list:
            lst.append(addentiy)
        for ntnm, arti, opt in lst:
            aft_msa.insert_entity(ntnm, arti, opt)
        return aft_msa

    def update_opt_deletenti(self, aft_msa):
        #make list to check
        lst_enti = []
        print(aft_msa.entity_list)
        for entity, arity, opt in aft_msa.entity_list:
            lst_enti.append(entity)
        #process
        Flag = True
        while Flag:
            want_delete = input("Type name of entity you want to delete")
            to_delete = []
            if want_delete in lst_enti:
                for entity, arity, opt in aft_msa.entity_list:
                    if entity == want_delete:
                        to_delete.append(entity)
                        to_delete.append(arity)
                        to_delete.append(opt)
                        break
                aft_msa.remove_entity(to_delete)
                lst_enti.remove(want_delete)
            else:
                print("no such thing entity that you type  "+want_delete)
            Flag = self.YN_Choice_menu("Did you want to delete more?")

        return aft_msa

    def update_opt_modienti(self, aft_msa, selected):
        #make list to check
        lst_enti = []
        for entity, arity, opt in aft_msa.entity_list:
            lst_enti.append(entity)
        #process
        model = self.import_system_entity_structure(self.model_db[selected])
        print(model)
        Flag = True
        while Flag:
            want_modify = input("Type name of entity you want to modify")
            if want_modify in lst_enti:
                _menu_number = self.update_opt_modienti_menu()
                if _menu_number == "1":
                    modi_name = input("Type name")
                    aft_msa.entity_list[lst_enti.index(want_modify)][0] = modi_name
                elif _menu_number == "2":
                    modi_arti = input("Type attribute")
                    aft_msa.entity_list[lst_enti.index(want_modify)][1] = modi_arti
                elif _menu_number == "3":
                    modi_opt = self.YN_Choice_menu("Is it optional?")
                    aft_msa.entity_list[lst_enti.index(want_modify)][2] = modi_opt
                elif _menu_number == "0":
                    break
            else:
                print("no such thing entity that you type  "+want_modify)
            Flag = self.YN_Choice_menu("Did you want to modify more?")

        return aft_msa

    def update_opt_modienti_menu(self):
        print("What process did you want to modify with this entity?")
        print("1.name")
        print("2. attribute")
        print("3. optional")
        print("0. Exit")
        selected = input(">>")
        return selected

    def update_opt_modiport(self, aft_msa):
        print(aft_msa.input_ports)
        print(aft_msa.output_ports)
        print(aft_msa.external_input_map)
        print(aft_msa.external_output_map)
        print(aft_msa.internal_coupling_map_entity)
        _menu_number = self.update_opt_modiport_menu()
        pass

    def update_opt_modiport_menu(self):
        print("What did you want to modify?")
        print("1.insert port")
        print("2.output port")
        print("3.external port")
        print("4.internal port")
        print("0. Exit")
        selected = input(">>")
        return selected

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

