from system_manager.system_manager import *
import os
import pymongo


class telegram_synthesisManager:
    def __init__(self):
        self.operation_count = 0
        self.glob_lst = {}
        self.entity_path = "./sample/ses_db"
        self.pes_db_path = './sample/pes_db'
        self.sm = SystemManager("./sample/ses_db", "./sample/model_db", './sample/pes_db')
        self.entity_db = []
        self.model_db = {}
        self.pes_db_map = {}
        self.make_db()

        self.selected = ""
        self.char_memo_1 = ""
        self.char_memo_2 = ""
        self.char_memo_3 = ""
        self.char_memo_4 = ""
        self.char_memo_5 = ""
        self.int_memo = 0
        self.list_memo = []
        self.list_memo_2 = []

        self.esm = None
        self.entity = None
        self.aft_msa = None

        self.pes = None
        self.ra = None
        self.mongo = None

    def make_db(self):
        self. entity_db = [f for f in listdir(self.entity_path) if isfile(join(self.entity_path, f))]
        for _file in self.entity_db:
            self.model_db[_file[:-5]] = os.path.join(os.path.abspath(self.entity_path), _file)

        for _file in [f for f in listdir(self.pes_db_path) if isfile(join(self.pes_db_path, f))]:
            self.pes_db_map[_file[:-5]] = os.path.join(os.path.abspath(self.pes_db_path), _file)

    def _list_pes(self, update):
        fmt = "{0: <13}\t{1: <13}"
        update.message.reply_text(fmt.format("PES Name", "Path"))
        st = ""
        for k, v in self.pes_db_map.items():
            st += fmt.format(k, v) + "\n"
        update.message.reply_text(st)

    def clear_system(self):
        self.glob_lst = {}
        self.operation_count = 0
        self.selected = ""
        self.mongo = None
        self.clear_memo()

    def clear_memo(self):
        self.char_memo_1 = ""
        self.char_memo_2 = ""
        self.char_memo_3 = ""
        self.char_memo_4 = ""
        self.char_memo_5 = ""
        self.int_memo = 0
        self.list_memo = []
        self.list_memo_2 = []

    def load_mongo(self):
        conn = pymongo.MongoClient('localhost', 27017)
        db = conn.get_database('pes_db')
        self.mongo = db.get_collection(self.selected)

    def load_entity(self, selected):
        self.esm = EntityManager()
        self.entity = self.esm.create_entity_structure()

        json_data = open(self.model_db[selected]).read()
        data = json.loads(json_data)
        self.aft_msa = ModelStructuralAttribute()
        self.entity.set_name(selected)
        core = data["core_attribute"]
        for ntnm, arti, opt in core["entities"]:
            self.aft_msa.insert_entity(ntnm, arti, opt)
        self.aft_msa.input_ports = core["input_ports"]
        self.aft_msa.output_ports = core["output_ports"]
        self.aft_msa.external_input_map = core["external_input"]
        self.aft_msa.external_output_map = core["external_output"]
        self.aft_msa.internal_coupling_map_entity = core["internal"]
        map_tuple = {}
        for key, item in core["internal"].items():
            in_lst = []
            for inoutlst in item:
                out_tpl = (key, inoutlst[0])
                in_tpl = (inoutlst[1][0], inoutlst[1][1])
                in_lst.append(in_tpl)
                map_tuple[out_tpl] = in_lst
        self.aft_msa.internal_coupling_map_tuple = map_tuple

    def save_entity(self):
        esm = EntityManager()
        entity = esm.create_entity_structure()
        entity.set_core_attribute(self.aft_msa)
        esm.create_system(entity)
        esm.export_system_entity_structure(entity, self.entity_path, self.selected + ".json")

    def YN_again_menu(self, update, restart_num):
        if update.message.text == "y":
            self.operation_count -= restart_num
            return False
        elif update.message.text == "n":
            self.operation_count += 1
            return True
        else:
            update.message.reply_text("[ERR] Please type only y or n")
            return False

    def YN_nextstep_menu(self, update, nextstep_num):
        if update.message.text == "y":
            self.operation_count += 1
            return True
        elif update.message.text == "n":
            self.operation_count += nextstep_num
            return False
        else:
            update.message.reply_text("[ERR] Please type only y or n")
            return False

    def Chk_int(self, update, _num):
        try:
            int(_num)
            return True
        except ValueError:
            update.message.reply_text("[ERR] Please type int")
            return False

    def print_entity_db(self,update):
        fmt = "{0: <13}\t{1: <13}"
        st = ""
        for k, v in self.model_db.items():
            st += fmt.format(k, v) + "\n"
        update.message.reply_text(st)

    def print_entity_information(self, update, target):
        fmt = "{0: <10}{name: <15}\t{arity: <5}\t{opt: <5}"
        _str = ""
        _str += "Name: " + target.entity_name + "\n"
        _str += fmt.format("Entities: ", name="Name", arity="Arity", opt="Optional") + "\n"
        entities = target.core_attribute.retrieve_entities()

        for idx, entity in enumerate(entities):
            _str += "\t" + fmt.format(idx+1, name=entity[0], arity=entity[1], opt=entity[2]) + "\n"

        update.message.reply_text(_str)

    def print_prunned_information(self, update):
        fmt = "{0: <10}{name: <15}\t{arity: <5}\t{opt: <5}"
        _str = ""
        _str += fmt.format("Entities: ", name="Name", arity="Arity", opt="Optional") + "\n"

        pruned = self.mongo.find()

        for idx, entity in enumerate(pruned):
            _str += "\t" + fmt.format(idx+1, name=entity['name'], arity=entity['arity'], opt=entity['opt']) + "\n"

        update.message.reply_text(_str)



    def interactive_pruning(self, update):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                self.selected = update.message.text
                self.load_entity(self.selected)
                root_entity = self.sm.esm.import_system_entity_structure(self.model_db[self.selected])
                self.pes = root_entity.clone()
                self.selected = "pruned_" + update.message.text
                self.pes.set_name(self.selected)
                self.pes.entity_list = self.pes.check_validity()
                self.load_mongo()

                update.message.reply_text("Type anything to process")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found")
                update.message.reply_text("Type name of Entity")
        elif self.operation_count == 2:
            fmt = "{name: <10}\t{arity: <5}\t{opt: <5}"
            update.message.reply_text("List of entities to pruning")
            _str = ""
            for entity in self.pes.entity_list:
                _str += fmt.format(name=entity[0], arity=entity[1], opt=entity[2]) + "\n"
            update.message.reply_text(_str)
            update.message.reply_text("Select entity to prune")
            self.operation_count += 1

        elif self.operation_count == 3:
            if True in list(map(lambda x: x[0] == update.message.text, self.pes.entity_list)):
                self.char_memo_1 = update.message.text
                update.message.reply_text("Type anything to process")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found. Please type again")

        elif self.operation_count == 4:
            for entity in self.pes.entity_list:
                if entity[0] == self.char_memo_1:
                    if entity[2]:
                        update.message.reply_text("> The sub-entity {0} is optional".format(entity[0]))
                        update.message.reply_text("> Select(s), Remove(n)")
                        self.operation_count += 1
                    else:
                        for entity in self.pes.entity_list:
                            if entity[0] == self.char_memo_1:
                                if type(entity[1]) is str:
                                    update.message.reply_text("> The arity of {0} is {1}".format(entity[0], entity[1]))
                                    update.message.reply_text("> Enter arity:")
                        self.operation_count += 2

        elif self.operation_count == 5:
            for entity in self.pes.entity_list:
                if entity[0] == self.char_memo_1:
                    if update.message.text == 's':
                        entity[2] = False
                        if type(entity[1]) is str:
                            update.message.reply_text("> The arity of {0} is {1}".format(entity[0], entity[1]))
                            update.message.reply_text("> Enter arity:")
                        self.operation_count += 1
                    elif update.message.text == 'n':
                        self.list_memo = entity
                        update.message.reply_text("Enter anything to continue")
                        self.operation_count += 2
                    else:
                        update.message.reply_text("Please type only s or n")
                        update.message.reply_text("> Select(s), Remove(n)")

        elif self.operation_count == 6:
            for entity in self.pes.entity_list:
                if entity[0] == self.char_memo_1:
                    entity[1] = int(update.message.text)
                    update.message.reply_text("Enter anything to continue")
                    self.operation_count += 1

        elif self.operation_count == 7:
            if len(self.list_memo) > 0:
                self.pes.core_attribute.remove_entity(self.list_memo)
                self.list_memo = []
            self.pes.entity_list = self.pes.check_validity()
            if not len(self.pes.entity_list) == 0:
                fmt = "{name: <10}\t{arity: <5}\t{opt: <5}"
                update.message.reply_text("List of entities to pruning")
                _str = ""
                for entity in self.pes.entity_list:
                    _str += fmt.format(name=entity[0], arity=entity[1], opt=entity[2]) + "\n"
                update.message.reply_text(_str)
                update.message.reply_text("Select entity to prune")
                self.operation_count -= 4
            else:
                update.message.reply_text("Do you want to synthesize executable? (y/n)")
                self.operation_count += 1

        elif self.operation_count == 8:
            if self.YN_nextstep_menu(update, 6):
                self.ra = RuntimeAttribute()
                self.list_memo = self.pes.get_core_attribute().retrieve_entities()
                self.int_memo = len(self.list_memo)
                update.message.reply_text("Press enter anything to continue.")
            else:
                if update.message.text == "n":
                    update.message.reply_text("Press enter anything to continue.")

        elif self.operation_count == 9:
            if not self.int_memo == 0:
                update.message.reply_text("Do you want to add model instance? (y/n)")
                self.operation_count += 1
            else:
                self.operation_count += 5
                update.message.reply_text("Press enter anything to continue.")

        elif self.operation_count == 10:
            if self.YN_nextstep_menu(update, 4):
                self.ra.insert_entity(self.list_memo[len(self.list_memo)-self.int_memo][0])
                update.message.reply_text(">>> Enter path of {}'s"
                              " model instance: ".format(self.list_memo[len(self.list_memo)-self.int_memo][0]))

        elif self.operation_count == 11:
            self.ra.insert_model_path(self.list_memo[len(self.list_memo)-self.int_memo][0], update.message.text)
            update.message.reply_text(">>> Do you want to add domain instance? (y/n)")
            self.operation_count += 1

        elif self.operation_count == 12:
            if self.YN_nextstep_menu(update, 2):
                update.message.reply_text(">>> Enter path of {}'s domain instance"
                                          ": ".format(self.list_memo[len(self.list_memo)-self.int_memo][0]))

        elif self.operation_count == 13:
            self.ra.insert_domain_path(self.list_memo[len(self.list_memo)-self.int_memo][0], update.message.text)
            self.int_memo -= 1
            if not self.int_memo == 0:
                update.message.reply_text("Press enter anything to continue.")
                self.operation_count -= 4
            else:
                update.message.reply_text("Press enter anything to continue.")
                self.operation_count += 1

        elif self.operation_count == 14:
            if not self.ra is None:
                self.pes.insert_attribute(self.ra)
            update.message.reply_text(">>> Pruned Entity Structure <<< ")

            fmt = "{0: <10}{name: <15}\t{arity: <5}\t{opt: <5}"
            _str = ""
            _str += "Name: " + self.pes.entity_name + "\n"
            _str += fmt.format("Entities: ", name="Name", arity="Arity", opt="Optional") + "\n"
            entities = self.pes.core_attribute.retrieve_entities()
            for idx, entity in enumerate(entities):
                _str += "\t" + fmt.format(idx + 1, name=entity[0], arity=entity[1], opt=entity[2]) + "\n"

            update.message.reply_text(_str)
            update.message.reply_text("Stored in pes_db")
            pes_path = os.path.join(os.path.dirname(self.entity_path), "pes_db")

            esm = EntityManager()
            entity = esm.create_entity_structure()
            entity.set_core_attribute(self.aft_msa)
            esm.create_system(entity)
            self.esm.export_system_entity_structure(self.pes, pes_path, self.pes.get_name() + ".json")

            for entity in entities:
                self.mongo.insert_one\
                    ({'name': entity[0], 'arity': entity[1], 'opt': entity[2]})
            self.clear_system()

    def print_pruned_entity(self, update):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                self.selected = update.message.text
                self.load_mongo()
                self.print_prunned_information(update)
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")

    def delete_pruned_entity(self, update):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                self.selected = update.message.text
                self.load_mongo()
                self.print_prunned_information(update)
                update.message.reply_text("Select entity to delete")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found")
        elif self.operation_count == 2:
            collection = self.mongo.find()
            for item in collection:
                self.list_memo.append(item['name'])
            if update.message.text in self.list_memo:
                self.mongo.delete_one({'name':update.message.text})
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")

    def update_pruned_entity_name(self, update):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                self.selected = update.message.text
                self.load_mongo()
                self.print_prunned_information(update)
                update.message.reply_text("Select entity to update")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found")
        elif self.operation_count == 2:
            collection = self.mongo.find()
            for item in collection:
                self.list_memo.append(item['name'])
            if update.message.text in self.list_memo:
                self.char_memo_1 = update.message.text
                update.message.reply_text("Enter the new name")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found")
        elif self.operation_count == 3:
            self.char_memo_2 = update.message.text
            update.message.reply_text("Enter the new attribute number")
            self.operation_count += 1
        elif self.operation_count == 4:
            if self.Chk_int(update,update.message.text):
                self.int_memo = int(update.message.text)
                update.message.reply_text("Is this optional? (y/n)")
                self.operation_count += 1
        elif self.operation_count == 5:
            if update.message.text == 'y':
                self.mongo.replace_one({'name': self.char_memo_1}, {'name': self.char_memo_2, 'arity': self.int_memo,
                                       'opt' : True})
                self.clear_system()
            elif update.message.text == 'n':
                self.mongo.replace_one({'name': self.char_memo_1}, {'name': self.char_memo_2, 'arity': self.int_memo,
                                       'opt' : False})
                self.clear_system()
            else:
                update.message.reply_text("Please enter only y or n")
