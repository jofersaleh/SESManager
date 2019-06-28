from system_manager.system_manager import *
import os
import sys
import pymongo


class telegram_executionManager:
    def __init__(self):
        self.operation_count = 0
        self.sm = SystemManager("./sample/ses_db", "./sample/model_db", './sample/pes_db')
        self.pes_db_path = './sample/pes_db'
        self.model_db_path = "./sample/model_db"
        self.pes_db_map = {}
        self.model_db_map = {}
        self.file_db_init()

        self.selected = ""
        self.char_memo_1 = ""
        self.char_memo_2 = ""
        self.char_memo_3 = ""
        self.char_memo_4 = ""
        self.char_memo_5 = ""
        self.int_memo = 0
        self.list_memo = []
        self.list_memo_2 = []
        self.es = None


        self.pes = None
        self.ra = None

    def file_db_init(self):
        for _file in [f for f in listdir(self.pes_db_path) if isfile(join(self.pes_db_path, f))]:
            self.pes_db_map[_file[:-5]] = os.path.join(os.path.abspath(self.pes_db_path), _file)

        for _file in [f for f in listdir(self.model_db_path) if isfile(join(self.model_db_path, f))]:
            self.model_db_map[_file[:-4]] = os.path.join(os.path.abspath(self.model_db_path), _file)

    def clear_system(self):
        self.operation_count = 0
        self.selected = ""
        self.es = None
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

    def _list_pes(self, update):
        fmt = "{0: <13}\t{1: <13}"
        update.message.reply_text(fmt.format("PES Name", "Path"))
        st = ""
        for k, v in self.pes_db_map.items():
            st += fmt.format(k, v) + "\n"
        update.message.reply_text(st)

    def _sim_start(self, update, context):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
            return
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                f = open("telegram_control/output.txt", 'w')
                stdout = sys.stdout
                sys.stdout = f

                entity_structure = \
                EntityManager.static_import_system_entity_structure(self.pes_db_map[update.message.text])
                SystemSimulator().register_engine(entity_structure.get_name())
                entities = entity_structure.get_core_attribute().retrieve_entities()
                instance_map = {}
                for entity in entities:
                    with open(self.model_db_map[entity[0]], 'rb') as f:
                        instance_map[entity[0]] = dill.load(f)
                        instance_map[entity[0]].set_engine_name(entity_structure.get_name())
                        SystemSimulator().get_engine(entity_structure.get_name()).register_entity(
                            instance_map[entity[0]])

                ic_map = entity_structure.get_core_attribute().retrieve_internal_coupling()
                for model, tup in ic_map.items():
                    SystemSimulator().get_engine(entity_structure.get_name()).coupling_relation(
                        instance_map[model], tup[0][0], instance_map[tup[0][1][0]], tup[0][1][1])

                SystemSimulator().get_engine(entity_structure.get_name()).simulate()
                self.clear_system()
                sys.stdout = stdout
                f.close()
                f = open("telegram_control/output.txt", "rb")
                context.bot.send_document(chat_id=update.message.chat_id, document=f)

            else:
                update.message.reply_text("[ERR] Entity Not Found")


    def _sys_exec(self, update):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
            return
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                es = \
                EntityManager.static_import_system_entity_structure(self.pes_db_map[update.message.text])
                SystemSimulator().register_engine(es.get_name())
                attributes = es.get_attribute_list()
                entities = es.get_core_attribute().retrieve_entities()

                ra = None
                for attr in attributes:
                    if attr.get_type() == AttributeType.RUNTIME:
                        ra = attr

                instance_map = {}
                if not ra:
                    for entity in entities:
                        with open(self.model_db_map[entity[0]], 'rb') as f:
                            instance_map[entity[0]] = dill.load(f)
                            instance_map[entity[0]].set_engine_name(es.get_name())
                            SystemSimulator().get_engine(es.get_name()).register_entity(instance_map[entity[0]])
                else:
                    entity_list = ra.retrieve_entities()
                    model_map = ra.retrieve_model_map()
                    domain_map = ra.retrieve_domain_map()

                    for entity in entity_list:
                        with open(model_map[entity], 'rb') as f:
                            instance_map[entity] = dill.load(f)
                        if entity in domain_map:
                            with open(domain_map[entity], 'rb') as f:
                                instance_map[entity].domain_obj = dill.load(f)

                        instance_map[entity].set_engine_name(es.get_name())
                        SystemSimulator().get_engine(es.get_name()).register_entity(instance_map[entity])

                ic_map = es.get_core_attribute().retrieve_internal_coupling()
                for model, tup in ic_map.items():
                    SystemSimulator().get_engine(es.get_name()).coupling_relation(
                        instance_map[model], tup[0][0], instance_map[tup[0][1][0]], tup[0][1][1])

                SystemSimulator().get_engine(es.get_name()).simulate()
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")

    def _sys_synthesis(self, update):
        if self.operation_count == 0:
            fmt = "{0: <13}\t{1: <13}"
            update.message.reply_text(fmt.format("PES Name", "Path"))
            st = ""
            for k, v in self.pes_db_map.items():
                st += fmt.format(k, v) + "\n"
            update.message.reply_text(st)
            update.message.reply_text("Select PES:")
            self.operation_count += 1
            return
        elif self.operation_count == 1:
            if update.message.text in self.pes_db_map:
                self.es = \
                EntityManager.static_import_system_entity_structure(self.pes_db_map[update.message.text])
                SystemSimulator().register_engine(self.es.get_name())
                attributes = self.es.get_attribute_list()
                entities = self.es.get_core_attribute().retrieve_entities()

                ra = None
                for attr in attributes:
                    if attr.get_type() == AttributeType.RUNTIME:
                        ra = attr

                instance_map = {}
                if not ra:
                    for entity in entities:
                        with open(self.model_db_map[entity[0]], 'rb') as f:
                            instance_map[entity[0]] = dill.load(f)
                            instance_map[entity[0]].set_engine_name(self.es.get_name())
                            SystemSimulator().get_engine(self.es.get_name()).register_entity(instance_map[entity[0]])
                else:
                    entity_list = ra.retrieve_entities()
                    model_map = ra.retrieve_model_map()
                    domain_map = ra.retrieve_domain_map()

                    for entity in entity_list:
                        with open(model_map[entity], 'rb') as f:
                            instance_map[entity] = dill.load(f)
                        if entity in domain_map:
                            with open(domain_map[entity], 'rb') as f:
                                instance_map[entity].domain_obj = dill.load(f)

                        instance_map[entity].set_engine_name(self.es.get_name())
                        print(instance_map[entity].get_engine_name())
                        SystemSimulator().get_engine(self.es.get_name()).register_entity(instance_map[entity])

                ic_map = self.es.get_core_attribute().retrieve_internal_coupling()
                for model, tup in ic_map.items():
                    SystemSimulator().get_engine(self.es.get_name()).coupling_relation(
                        instance_map[model], tup[0][0], instance_map[tup[0][1][0]], tup[0][1][1])

                update.message.reply_text("Enter simx Path: ")
                self.operation_count += 1
            else:
                update.message.reply_text("[ERR] Entity Not Found")

        elif self.operation_count == 2:
            with open(os.path.join(os.path.abspath(update.message.text), self.es.get_name() + ".simx"), 'wb') as f:
                dill.dump(SystemSimulator().get_engine(self.es.get_name()), f)
            self.clear_system()


