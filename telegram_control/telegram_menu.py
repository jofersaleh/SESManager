from system_manager.system_manager import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class Remote_telegram():
    def __init__(self):
        self.STATUS = ""
        self.operation_count = 0
        self.glob_lst = {}
        self.entity_path = "./sample/ses_db"

        self.sm = SystemManager("./sample/ses_db", "./sample/model_db", './sample/pes_db')

        self.entity_db = []
        self.model_db = {}
        self.make_db()

    def make_db(self):
        self. entity_db = [f for f in listdir(self.entity_path) if isfile(join(self.entity_path, f))]
        for _file in self.entity_db:
            self.model_db[_file[:-5]] = os.path.join(os.path.abspath(self.entity_path), _file)

    def clear_system(self):
        self.glob_lst = {}
        self.operation_count = 0

    def print_current_menu(self, update, current_num):
        if current_num == 1:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. Create new Entity")
                update.message.reply_text("2. Read Entity")
                update.message.reply_text("3. Update Entity")
                update.message.reply_text("4. Delete Entity")
                update.message.reply_text("0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.setting_step(update)
        elif current_num == 2:
            if len(self.STATUS) == 1:
                #model management
                update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.setting_step(update)

        elif current_num == "0":
            if self.STATUS == "":
                update.message.reply_text("over")
        else:
            update.message.reply_text(self.STATUS)

    def setting_step(self, update):
        if self.STATUS == "11":
            self.create_option(update)
        if self.STATUS == "12":
            self.read_option(update)

    def YN_again_menu(self, update, restart_num):
        if update.message.text == "y":
            self.operation_count -= restart_num
            return False
        elif update.message.text == "n":
            self.operation_count += 1
            return True
        else:
            update.message.reply_text("please type only y or n")
            return False

    def YN_nextstep_menu(self, update, nextstep_num):
        if update.message.text == "y":
            self.operation_count += 1
            return True
        elif update.message.text == "n":
            self.operation_count += nextstep_num
            return False
        else:
            update.message.reply_text("please type only y or n")
            return False

    def Chk_int(self, update, _num):
        try:
            int(_num)
            return True
        except ValueError:
            update.message.reply_text("please type int")
            return False

    def print_entity_db(self,update):
        fmt = "{0: <13}\t{1: <13}"
        for k,v in self.model_db.items():
            update.message.reply_text(fmt.format(k,v))

    def print_entity_information(self, update, target):
        fmt = "{0: <10}{name: <15}\t{arity: <5}\t{opt: <5}"
        _str = ""
        _str += "Name: " + target.entity_name + "\n"
        _str += fmt.format("Entities: ", name="Name", arity="Arity", opt="Optional") + "\n"
        entities = target.core_attribute.retrieve_entities()

        for idx, entity in enumerate(entities):
            _str += "\t" + fmt.format(idx+1, name=entity[0], arity=entity[1], opt=entity[2]) + "\n"

        update.message.reply_text(_str)


    def create_option(self, update):
        if self.operation_count == 0:
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1

        elif self.operation_count == 1:
            self.glob_lst["name"] = update.message.text
            update.message.reply_text("How many input port did system need")
            self.operation_count += 1

        elif self.operation_count == 2:
            if self.Chk_int(update, update.message.text):
                self.glob_lst["num_input_port"] = update.message.text
                update.message.reply_text("How many output port did system need")
                self.operation_count += 1

        elif self.operation_count == 3:
            if self.Chk_int(update, update.message.text):
                self.glob_lst["num_output_port"] = update.message.text
                update.message.reply_text("What is the entity name?")
                self.operation_count += 1

        elif self.operation_count == 4:
            if "entities name" in self.glob_lst.keys():
                self.glob_lst["entities name"].append(update.message.text)
            else:
                self.glob_lst["entities name"] = [update.message.text]
            update.message.reply_text("Type number of arity")
            self.operation_count += 1

        elif self.operation_count == 5:
            if self.Chk_int(update, update.message.text):
                if "attribute number" in self.glob_lst.keys():
                    self.glob_lst["attribute number"].append(update.message.text)
                else:
                    self.glob_lst["attribute number"] = [update.message.text]
                update.message.reply_text("is this entity optional? (y/n)")
                self.operation_count += 1

        elif self.operation_count == 6:
            if update.message.text == "y":
                self.operation_count += 1
                if "optional" in self.glob_lst.keys():
                    self.glob_lst["optional"].append(True)
                else:
                    self.glob_lst["optional"] = [True]
                update.message.reply_text("Did you need more entity? (y/n)")
            elif update.message.text == "n":
                self.operation_count += 1
                if "optional" in self.glob_lst.keys():
                    self.glob_lst["optional"].append(False)
                else:
                    self.glob_lst["optional"] = [False]
                update.message.reply_text("Did you need more entity? (y/n)")
            else:
                update.message.reply_text("please type only y or n")

        elif self.operation_count == 7:
            print(self.glob_lst)
            if self.YN_again_menu(update, 3):
                update.message.reply_text("did you want to make external input port? (y/n)")
            else:
                if update.message.text == "y":
                    update.message.reply_text("What is the entity name?")


        elif self.operation_count == 8:
            if self.YN_nextstep_menu(update, 5):
                update.message.reply_text("number of input port :" + self.glob_lst["num_input_port"])
                update.message.reply_text("type the 'number' of input port that you will use for external input port")
            else:
                if update.message.text == "n":
                    update.message.reply_text("did you want to make external output port? (y/n)")

        elif self.operation_count == 9:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_input_port"]):
                    if "ex_in_portnum" in self.glob_lst.keys():
                        self.glob_lst["ex_in_portnum"].append(update.message.text)
                    else:
                        self.glob_lst["ex_in_portnum"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("created entities: " + str(self.glob_lst["entities name"]))
                    update.message.reply_text("choose entity to connect with input port")
                else:
                    update.message.reply_text("please type again")

        elif self.operation_count == 10:
            if update.message.text in self.glob_lst["entities name"]:
                if "ex_in_entity" in self.glob_lst.keys():
                    self.glob_lst["ex_in_entity"].append(update.message.text)
                else:
                    self.glob_lst["ex_in_entity"] = [update.message.text]
                update.message.reply_text("number of input port :" + self.glob_lst["num_input_port"])
                update.message.reply_text(
                    "Type the 'number' of input port that you will use for " + update.message.text + " input port")
                self.operation_count += 1
            else:
                update.message.reply_text("please type name that you create")

        elif self.operation_count == 11:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_input_port"]):
                    if "ex_in_portenti" in self.glob_lst.keys():
                        self.glob_lst["ex_in_portenti"].append(update.message.text)
                    else:
                        self.glob_lst["ex_in_portenti"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("did you need more connection? (y/n)")
                else:
                    update.message.reply_text("please type again")

        elif self.operation_count == 12:
            print(self.glob_lst)
            if self.YN_again_menu(update, 3):
                update.message.reply_text("did you want to make external output port? (y/n)")
            else:
                if update.message.text == "y":
                    update.message.reply_text("number of input port :" + str(self.glob_lst["num_input_port"]))
                    update.message.reply_text(
                        "type the 'number' of input port that you will use for external input port")


        elif self.operation_count == 13:
            if self.YN_nextstep_menu(update, 5):
                update.message.reply_text("number of output port :" + str(self.glob_lst["num_output_port"]))
                update.message.reply_text("type the 'number' of output port that you will use for external output port")
            else:
                if update.message.text == "n":
                    update.message.reply_text("did you want to make external internal port? (y/n)")

        elif self.operation_count == 14:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_output_port"]):
                    if "ex_out_portnum" in self.glob_lst.keys():
                        self.glob_lst["ex_out_portnum"].append(update.message.text)
                    else:
                        self.glob_lst["ex_out_portnum"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("created entities: " + str(self.glob_lst["entities name"]))
                    update.message.reply_text("choose entity to connect with output port")
                else:
                    update.message.reply_text("please type again")

        elif self.operation_count == 15:
            if update.message.text in self.glob_lst["entities name"]:
                if "ex_out_entity" in self.glob_lst.keys():
                    self.glob_lst["ex_out_entity"].append(update.message.text)
                else:
                    self.glob_lst["ex_out_entity"] = [update.message.text]
                update.message.reply_text("number of output port :" + str(self.glob_lst["num_output_port"]))
                update.message.reply_text(
                    "Type the 'number' of output port that you will use for " + update.message.text + " output port")
                self.operation_count += 1
            else:
                update.message.reply_text("please type name that you create")

        elif self.operation_count == 16:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_output_port"]):
                    if "ex_out_portenti" in self.glob_lst.keys():
                        self.glob_lst["ex_out_portenti"].append(update.message.text)
                    else:
                        self.glob_lst["ex_out_portenti"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("did you need more connection? (y/n)")
                else:
                    update.message.reply_text("please type again")

        elif self.operation_count == 17:
            print(self.glob_lst)
            if self.YN_again_menu(update, 3):
                update.message.reply_text("did you want to make internal port? (y/n)")
            else:
                if update.message.text == "y":
                    update.message.reply_text("number of output port :" + str(self.glob_lst["num_output_port"]))
                    update.message.reply_text(
                        "type the 'number' of output port that you will use for external output port")

        elif self.operation_count == 18:
            if self.YN_nextstep_menu(update, 5):
                update.message.reply_text("created entities: " + str(self.glob_lst["entities name"]))
                update.message.reply_text("choose first entity out to other")
            else:
                if update.message.text == "n":
                    print(self.glob_lst)
        elif self.operation_count == 19:
            if update.message.text in self.glob_lst["entities name"]:
                if "internal_out_entity" in self.glob_lst.keys():
                    self.glob_lst["internal_out_entity"].append(update.message.text)
                else:
                    self.glob_lst["internal_out_entity"] = [update.message.text]
                update.message.reply_text("number of output port :" + str(self.glob_lst["num_output_port"]))
                update.message.reply_text(
                    "Type the 'number' of output port that you will use for " + update.message.text + " output port")
                self.operation_count += 1
            else:
                update.message.reply_text("please type name that you create")
        elif self.operation_count == 20:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_output_port"]):
                    if "internal_out_port" in self.glob_lst.keys():
                        self.glob_lst["internal_out_port"].append(update.message.text)
                    else:
                        self.glob_lst["internal_out_port"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("created entities: " + str(self.glob_lst["entities name"]))
                    update.message.reply_text("choose second entity in by other")
                else:
                    update.message.reply_text("please type again")
        elif self.operation_count == 21:
            if update.message.text in self.glob_lst["entities name"]:
                if "internal_in_entity" in self.glob_lst.keys():
                    self.glob_lst["internal_in_entity"].append(update.message.text)
                else:
                    self.glob_lst["internal_in_entity"] = [update.message.text]
                update.message.reply_text("number of input port :" + str(self.glob_lst["num_input_port"]))
                update.message.reply_text(
                    "Type the 'number' of input port that you will use for " + update.message.text + " input port")
                self.operation_count += 1
            else:
                update.message.reply_text("please type name that you create")
        elif self.operation_count == 22:
            if self.Chk_int(update, update.message.text):
                if float(update.message.text) <= float(self.glob_lst["num_input_port"]):
                    if "internal_in_port" in self.glob_lst.keys():
                        self.glob_lst["internal_in_port"].append(update.message.text)
                    else:
                        self.glob_lst["internal_in_port"] = [update.message.text]
                    self.operation_count += 1
                    update.message.reply_text("Did you need more connection? (y/n)")
                else:
                    update.message.reply_text("please type again")

        elif self.operation_count == 23:
            print(self.glob_lst)
            if self.YN_again_menu(update, 4):
                esm = EntityManager()
                msa = ModelStructuralAttribute()
                entity = esm.create_entity_structure()
                entity.set_name(self.glob_lst["name"])
                if int(self.glob_lst["num_input_port"]) >0:
                    for i in range(int(self.glob_lst["num_input_port"])):
                            nm = "in"+str(i+1)
                            msa.insert_input_port(nm)
                if int(self.glob_lst["num_output_port"]) > 0:
                    for i in range(int(self.glob_lst["num_output_port"])):
                            nm = "out"+str(i+1)
                            msa.insert_input_port(nm)
                for i in range(len(self.glob_lst["entities name"])):
                    msa.insert_entity(self.glob_lst["entities name"][i], self.glob_lst["attribute number"][i],
                                      self.glob_lst["optional"][i])
                if len(self.glob_lst["ex_in_portnum"]) > 0:
                    for i in range(len(self.glob_lst["ex_in_portnum"])):
                        msa.insert_coupling(("", self.glob_lst["ex_in_portnum"][i]), (self.glob_lst["ex_in_entity"][i],
                                                                                   self.glob_lst["ex_in_portenti"][i]))
                if len(self.glob_lst["ex_out_portnum"]) > 0:
                    for i in range(len(self.glob_lst["ex_out_portnum"])):
                        msa.insert_coupling((self.glob_lst["ex_out_entity"][i], self.glob_lst["ex_out_portenti"][i]),
                                            ("", self.glob_lst["ex_out_portnum"][i]))
                if len(self.glob_lst["internal_out_entity"]) > 0:
                    for i in range(len(self.glob_lst["internal_out_entity"])):
                        msa.insert_coupling((self.glob_lst["internal_out_entity"][i],
                                             self.glob_lst["internal_out_port"][i]),
                                            (self.glob_lst["internal_in_entity"][i],
                                             self.glob_lst["internal_in_port"][i]))
                entity.set_core_attribute(msa)
                esm.create_system(entity)
                esm.export_system_entity_structure(entity, self.entity_path, str(self.glob_lst["name"]) + ".json")

                self.clear_system()

            else:
                if update.message.text == "y":
                    update.message.reply_text("created entities: " + str(self.glob_lst["entities name"]))
                    update.message.reply_text("choose first entity out to other")

    def read_option(self, update):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                model = self.sm.esm.import_system_entity_structure(self.model_db[update.message.text])
                print(model)
                self.print_entity_information(update, model)
                #update.message.reply_text(model)
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")
                update.message.reply_text("Type name of Entity")


