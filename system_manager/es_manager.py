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

    def Num_Choice_menu(self, put_num, set_num):
        if self.Chk_int(put_num):
            put_num = int(put_num)
            Flag = False
        else:
            return put_num, True
        if put_num > set_num or put_num <= 0:
            print("please type again")
            Flag = True
        return put_num, Flag


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
        inptnum = 0
        outptnum = 0

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
        ask = self.YN_Choice_menu("Did you want to make external input port?")
        if ask == True:
            Tot_Flag = True
            while Tot_Flag:
                num_port = 0
                Flag = True
                while Flag:
                    print("Number of input port: ", inptnum)
                    num_port = input("type the 'number' of input port that you will use for external input port")
                    num_port, Flag = self.Num_Choice_menu(num_port, inptnum)
                Flag = True
                while Flag:
                    print(list_entity_nm)
                    input_entity = input("choose entity to connect with input port")
                    if input_entity in list_entity_nm:
                        ex_input_port = "in" + str(num_port)
                        loop = True
                        while loop:
                            print("Number of input port: ", inptnum)
                            num_port = input("Type the 'number' of input port that you will use for "+input_entity + " input port")
                            num_port, loop = self.Num_Choice_menu(num_port, inptnum)
                        input_port = "in" + str(num_port)
                        msa.insert_coupling(("", ex_input_port), (input_entity, input_port))
                        Flag = False
                    else:
                        print("Not in a list. Please type again")
                Tot_Flag = self.YN_Choice_menu("did you need more connection?")
        ask = self.YN_Choice_menu("Did you want to make external output port?")
        if ask == True:
            Tot_Flag = True
            while Tot_Flag:
                num_port = 0
                Flag = True
                while Flag:
                    print("Number of output port: ", outptnum)
                    num_port = input("type the 'number' of output port that you will use for external output port")
                    num_port, Flag = self.Num_Choice_menu(num_port, outptnum)
                Flag = True
                while Flag:
                    print(list_entity_nm)
                    output_entity = input("choose entity to connect with output port")
                    if output_entity in list_entity_nm:
                        ex_output_port = "out" + str(num_port)
                        loop = True
                        while loop:
                            print("Number of output port: ", outptnum)
                            num_port = input("Type the 'number' of output port that you will use for "+output_entity + " output port")
                            num_port, loop = self.Num_Choice_menu(num_port, outptnum)
                        output_port = "out" + str(num_port)
                        msa.insert_coupling((output_entity, output_port), ("", ex_output_port))
                        Flag = False
                    else:
                        print("Not in a list. Please type again")
                Tot_Flag = self.YN_Choice_menu("did you need more connection?")
        ask = self.YN_Choice_menu("Did you want to make internal port?")
        if ask == True:
            Flag = True
            while Flag:
                loop = True
                while loop:
                    print(list_entity_nm)
                    interaction_entity1 = input("choose first entity out to other")
                    if interaction_entity1 in list_entity_nm:
                        loop = False
                    else:
                        print("not in the list. please type again.")
                loop = True
                while loop:
                    print("Number of output port: ", outptnum)
                    num_port = input("type the 'number' of output port that you will use for " + interaction_entity1)
                    num_port, loop = self.Num_Choice_menu(num_port, outptnum)
                    interaction_outport = "out" + str(num_port)
                loop = True
                while loop:
                    print(list_entity_nm)
                    interaction_entity2 = input("choose second entity in by other")
                    if interaction_entity2 in list_entity_nm:
                        loop = False
                    else:
                        print("not in the list. please type again.")
                loop = True
                while loop:
                    print("Number of output port: ", inptnum)
                    num_port = input("type the 'number' of input port that you will use for " + interaction_entity2)
                    num_port, loop = self.Num_Choice_menu(num_port, inptnum)
                    interaction_inport = "in" + str(num_port)
                msa.insert_coupling((interaction_entity1, interaction_outport), (interaction_entity2, interaction_inport))
                Flag = self.YN_Choice_menu("did you need more connection?")

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
        map_tuple = {}
        for key, item in core["internal"].items():
            in_lst = []
            for inoutlst in item:
                out_tpl = (key, inoutlst[0])
                in_tpl = (inoutlst[1][0], inoutlst[1][1])
                in_lst.append(in_tpl)
                map_tuple[out_tpl] = in_lst
        aft_msa.internal_coupling_map_tuple = map_tuple

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
                    aft_msa = self.update_opt_modiport(aft_msa)
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
        print("input port: ", aft_msa.input_ports)
        print("output port: ", aft_msa.output_ports)
        print("external input: ", aft_msa.external_input_map)
        print("external output: ", aft_msa.external_output_map)
        print("internal: ", aft_msa.internal_coupling_map_entity)
        print("internal: ", aft_msa.internal_coupling_map_tuple)

        Flag = True

        while Flag:
            _menu_number = self.update_opt_modiport_menu()
            if _menu_number == "1":
                loop = True
                while loop:
                    _sub_number = self.update_opt_modiport_insertport_menu()
                    if _sub_number == "1":
                        port_name = input("Type the name of port")
                        aft_msa.insert_input_port(port_name)
                    elif _sub_number == "2":
                        port_name = input("Type the name of port")
                        aft_msa.insert_output_port(port_name)
                    elif _sub_number == "3":
                        print(aft_msa.input_ports)
                        Flag = True
                        while Flag:
                            port_name_external = input(
                                "type the name of input port that you will use for external input port")
                            if port_name_external in aft_msa.input_ports:
                                Flag = False
                            else:
                                print("there is no such " + port_name_external + " please type again.")
                        list_entity = []
                        for name, arti, opt in aft_msa.entity_list:
                            list_entity.append(name)
                        Flag = True
                        while Flag:
                            print(list_entity)
                            input_entity = input("choose entity to connect with input port")
                            if input_entity in list_entity:
                                loop = True
                                while loop:
                                    print(aft_msa.input_ports)
                                    input_port = input(
                                        "Type the name of input port that you will use for " + input_entity + " input port")
                                    if input_port in aft_msa.input_ports:
                                        loop = False
                                    else:
                                        print("there is no such " + input_port + " please type again.")
                                aft_msa.insert_coupling(("", port_name_external), (input_entity, input_port))
                                Flag = False
                            else:
                                print("Not in a list. Please type again")
                    elif _sub_number == "4":
                        print(aft_msa.output_ports)
                        Flag = True
                        while Flag:
                            port_name_external = input(
                                "type the name of input port that you will use for external input port")
                            if port_name_external in aft_msa.output_ports:
                                Flag = False
                            else:
                                print("there is no such " + port_name_external + " please type again.")
                        list_entity = []
                        for name, arti, opt in aft_msa.entity_list:
                            list_entity.append(name)
                        Flag = True
                        while Flag:
                            print(list_entity)
                            output_entity = input("choose entity to connect with output port")
                            if output_entity in list_entity:
                                loop = True
                                while loop:
                                    print(aft_msa.output_ports)
                                    output_port = input(
                                        "Type the name of input port that you will use for " + output_entity + " output port")
                                    if output_port in aft_msa.output_ports:
                                        loop = False
                                    else:
                                        print("there is no such " + output_port + " please type again.")
                                aft_msa.insert_coupling((output_entity, output_port), ("", port_name_external))
                                Flag = False
                            else:
                                print("Not in a list. Please type again")
                    elif _sub_number == "5":
                        list_entity = []
                        Flag = True
                        for name, arti, opt in aft_msa.entity_list:
                            list_entity.append(name)
                        while Flag:
                            loop = True
                            while loop:
                                print(list_entity)
                                interaction_entity1 = input("choose first entity out to other")
                                if interaction_entity1 in list_entity:
                                    loop = False
                                else:
                                    print("not in the list. please type again.")
                            loop = True
                            while loop:
                                print(aft_msa.output_ports)
                                output_port = input(
                                    "Type the name of output port that you will use for " + interaction_entity1 + " output port")
                                if output_port in aft_msa.output_ports:
                                    loop = False
                                else:
                                    print("there is no such " + output_port + " please type again.")
                            loop = True
                            while loop:
                                print(list_entity)
                                interaction_entity2 = input("choose second entity in by other")
                                if interaction_entity2 in list_entity:
                                    loop = False
                                else:
                                    print("not in the list. please type again.")
                            loop = True
                            while loop:
                                print(aft_msa.input_ports)
                                input_port = input(
                                    "Type the name of output port that you will use for " + interaction_entity2 + " input port")
                                if input_port in aft_msa.input_ports:
                                    loop = False
                                else:
                                    print("there is no such " + input_port + " please type again.")
                            aft_msa.insert_coupling((interaction_entity1, output_port),
                                                (interaction_entity2, input_port))
                            Flag = self.YN_Choice_menu("did you need more connection?")
                    elif _sub_number == "0":
                        loop = False
                    else:
                        print("please type again")
            elif _menu_number == "2":
                loop = True
                while loop:
                    _sub_number = self.update_opt_modiport_deleteport_menu()
                    if _sub_number == "1":
                        Flag = True
                        while Flag:
                            print(aft_msa.input_ports)
                            port_name = input("Type port that you want to delete")
                            if port_name in aft_msa.input_ports:
                                aft_msa.input_ports.remove(port_name)
                                if port_name in aft_msa.external_input_map.keys():
                                    aft_msa.external_input_map.pop(port_name)
                                pop_lst = []
                                for key, values in aft_msa.external_input_map.items():
                                    rmv_lst = []
                                    i = len(values)
                                    for item in values:
                                        if item[1] == port_name:
                                            if i == 1:
                                                pop_lst.append(key)
                                            else:
                                                rmv_lst.append(item)
                                                i -= 1
                                    for item in rmv_lst:
                                        values.remove(item)
                                for key in pop_lst:
                                    aft_msa.external_input_map.pop(key)
                                pop_lst = []
                                for key, values in aft_msa.internal_coupling_map_entity.items():
                                    rmv_lst = []
                                    i = len(values)
                                    for item in values:
                                        if item[1][1] == port_name:
                                            if i == 1:
                                                pop_lst.append(key)
                                            else:
                                                rmv_lst.append(item)
                                                i -= 1
                                    for item in rmv_lst:
                                        values.remove(item)
                                for key in pop_lst:
                                    aft_msa.internal_coupling_map_entity.pop(key)
                                pop_lst = []
                                for key, values in aft_msa.internal_coupling_map_tuple.items():
                                    rmv_lst = []
                                    i = len(values)
                                    for item in values:
                                        if item[1] == port_name:
                                            if len(values) == 1:
                                                pop_lst.append(key)
                                            else:
                                                rmv_lst.append(item)
                                                i -= 1
                                    for item in rmv_lst:
                                        values.remove(item)
                                for key in pop_lst:
                                    aft_msa.internal_coupling_map_tuple.pop(key)
                                Flag = False
                            else:
                                print("No such name " + port_name + "please type again.")
                    elif _sub_number == "2":
                        Flag = True
                        while Flag:
                            print(aft_msa.output_ports)
                            port_name = input("Type port that you want to delete")
                            if port_name in aft_msa.output_ports:
                                aft_msa.output_ports.remove(port_name)
                                if port_name in aft_msa.external_output_map.keys():
                                    aft_msa.external_output_map.pop(port_name)
                                pop_lst = []
                                for key, values in aft_msa.external_output_map.items():
                                    rmv_lst = []
                                    i = len(values)
                                    for item in values:
                                        if item[1] == port_name:
                                            if i == 1:
                                                pop_lst.append(key)
                                            else:
                                                rmv_lst.append(item)
                                                i -= 1
                                    for item in rmv_lst:
                                        values.remove(item)
                                for key in pop_lst:
                                    aft_msa.external_output_map.pop(key)
                                pop_lst = []
                                for key, values in aft_msa.internal_coupling_map_entity.items():
                                    rmv_lst = []
                                    i = len(values)
                                    for item in values:
                                        if item[0] == port_name:
                                            if i == 1:
                                                pop_lst.append(key)
                                            else:
                                                rmv_lst.append(item)
                                                i -= 1
                                    for item in rmv_lst:
                                        values.remove(item)
                                for key in pop_lst:
                                    aft_msa.internal_coupling_map_entity.pop(key)
                                pop_lst = []
                                for key, values in aft_msa.internal_coupling_map_tuple.items():
                                    if key[1] == port_name:
                                        pop_lst.append(key)
                                for key in pop_lst:
                                    aft_msa.internal_coupling_map_tuple.pop(key)
                                Flag = False
                            else:
                                print("No such name " + port_name + "please type again.")
                    elif _sub_number == "3":
                        print(aft_msa.external_input_map.keys())
                        port_name = input("Type input port that you want to delete")
                        if len(aft_msa.external_input_map.get(port_name)) == 1:
                            aft_msa.remove_coupling(("", port_name), (aft_msa.external_input_map.get(port_name)[0][0],
                                                                      aft_msa.external_input_map.get(port_name)[0][1]))
                        else:
                            print(aft_msa.external_input_map.values())
                            enti_name = input("Type name the name of the entity")
                            i = 0
                            T = True
                            while T:
                                _compared = aft_msa.external_input_map.get(port_name)[i][0]
                                if _compared == enti_name:
                                    T = False
                                else:
                                    i += 1
                            aft_msa.remove_coupling(("", port_name), (aft_msa.external_input_map.get(port_name)[i][0],
                                                                      aft_msa.external_input_map.get(port_name)[i][1]))
                    elif _sub_number == "4":
                        print(aft_msa.external_output_map.keys())
                        port_name = input("Type output port that you want to delete")
                        if len(aft_msa.external_output_map.get(port_name)) == 1:
                            aft_msa.remove_coupling((aft_msa.external_output_map.get(port_name)[0][0],
                                                     aft_msa.external_output_map.get(port_name)[0][1]), ("", port_name))
                        else:
                            print(aft_msa.external_output_map.values())
                            enti_name = input("Type name the name of the entity")
                            i = 0
                            T = True
                            while T:
                                _compared = aft_msa.external_output_map.get(port_name)[i][0]
                                if _compared == enti_name:
                                    T = False
                                else:
                                    i += 1
                            aft_msa.remove_coupling(("", port_name), (aft_msa.external_output_map.get(port_name)[i][0],
                                                                      aft_msa.external_output_map.get(port_name)[i][1]))
                    elif _sub_number == "5":
                        print(aft_msa.internal_coupling_map_tuple)
                        port_name1 = input("Type output port that you want to delete")
                        port_name2 = input("Type input port that you want to delete")
                        enti_name1 = input("Type output entity that you want to delete")
                        enti_name2 = input("Type input entity that you want to delete")
                        aft_msa.remove_coupling((enti_name1, port_name1), (enti_name2, port_name2))
                    elif _sub_number == "0":
                        loop = False
                    else:
                        print("please type again")
            elif _menu_number == "3":
                loop = True
                while loop:
                    _sub_number = self.update_opt_modiport_changename()
                    if _sub_number == "1":
                        print(aft_msa.input_ports)
                        bef_name = input("Type name of input port that you want to change")
                        aft_name = input("Type the new name of port")
                        if bef_name in aft_msa.input_ports:
                            aft_msa.input_ports[aft_msa.input_ports.index(bef_name)] = aft_name
                            if bef_name in aft_msa.external_input_map.keys():
                                aft_msa.external_input_map[aft_name] = aft_msa.external_input_map.pop(bef_name)
                            for item in aft_msa.external_input_map.values():
                                for i in range(len(item)):
                                    if item[i][1] == bef_name:
                                        item[i][1] = aft_name
                            for item in aft_msa.internal_coupling_map_entity.values():
                                for i in range(len(item)):
                                    if item[i][1][1] == bef_name:
                                        item[i][1][1] = aft_name
                            for item in aft_msa.internal_coupling_map_tuple.values():
                                for i in range(len(item)):
                                    if bef_name == item[i][1]:
                                        e = item[i][0]
                                        item[i] = (e, aft_name)
                        else:
                            print("No such " + bef_name + "in the port")
                    elif _sub_number == "2":
                        print(aft_msa.output_ports)
                        bef_name = input("Type name of input port that you want to change")
                        aft_name = input("Type the new name of port")
                        if bef_name in aft_msa.output_ports:
                            aft_msa.output_ports[aft_msa.output_ports.index(bef_name)] = aft_name
                            if bef_name in aft_msa.external_output_map.keys():
                                aft_msa.external_output_map[aft_name] = aft_msa.external_output_map.pop(bef_name)
                            for item in aft_msa.external_output_map.values():
                                for i in range(len(item)):
                                    if item[i][1] == bef_name:
                                        item[i][1] = aft_name
                            for item in aft_msa.internal_coupling_map_entity.values():
                                for i in range(len(item)):
                                    if item[i][0] == bef_name:
                                        item[i][0] = aft_name
                            for item in aft_msa.internal_coupling_map_tuple.keys():
                                for i in range(int(len(item)/2)):
                                    if bef_name == item[i*2+1]:
                                        aft_msa.internal_coupling_map_tuple[item[i], aft_name] = aft_msa.internal_coupling_map_tuple.pop(item)
                        else:
                            print("please type again")
                    elif _sub_number == "0":
                        loop = False
                    else:
                        print("please type again")
            elif _menu_number == "0":
                Flag = False
            else:
                print("please type again")
        return aft_msa


    def update_opt_modiport_menu(self):
        print("What did you want to modify?")
        print("1.insert new port")
        print("2.delete port")
        print("3.change name of port")
        print("0. Exit")
        selected = input(">>")
        return selected

    def update_opt_modiport_insertport_menu(self):
        print("What did you want to insert?")
        print("1. input port")
        print("2. output port")
        print("3. external input port")
        print("4. external output port")
        print("5. internal")
        print("0. Exit")
        selected = input(">>")
        return selected

    def update_opt_modiport_deleteport_menu(self):
        print("What did you want to delete?")
        print("1. input port")
        print("2. output port")
        print("3. external input port")
        print("4. external output port")
        print("5. internal")
        print("0. Exit")
        selected = input(">>")
        return selected

    def update_opt_modiport_changename(self):
        print("What port did you want to change?")
        print("1. input port")
        print("2. output port")
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

