import pydot
from system_manager.system_manager import *
from io import BytesIO
from graphviz import Digraph
from PIL import Image
#from IPython.core.display import Image
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'


class telegram_dotManager:
    def __init__(self):
        self.operation_count = 0
        self.entity_path = "./sample/ses_db"
        self.sm = SystemManager("./sample/ses_db", "./sample/model_db", './sample/pes_db')
        self.entity_db = []
        self.model_db = {}
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

    def clear_system(self):
        self.operation_count = 0
        self.selected = ""
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

    def make_db(self):
        self. entity_db = [f for f in listdir(self.entity_path) if isfile(join(self.entity_path, f))]
        for _file in self.entity_db:
            self.model_db[_file[:-5]] = os.path.join(os.path.abspath(self.entity_path), _file)

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

    def print_entity_db(self,update):
        fmt = "{0: <13}\t{1: <13}"
        st = ""
        for k, v in self.model_db.items():
            st += fmt.format(k, v) + "\n"
        update.message.reply_text(st)

    def send_dot_telegram(self, user_dot, update, context):
        user_dot.format = 'png'
        image_render = user_dot.render(view=False)
        img = Image.open(image_render)
        img = img.convert('RGB')
        bio = BytesIO()
        bio.name = 'image.jpeg'
        img.save(bio, 'JPEG')
        bio.seek(0)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=bio)

    def print_entity_dot(self, update, context):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                self.selected = update.message.text
                self.load_entity(self.selected)
                command = Digraph(comment=self.entity.entity_name)
                command.node('R', self.entity.entity_name, shape="box")

                for i in range(len(self.aft_msa.entity_list)):
                    if self.aft_msa.entity_list[i][2]:
                        command.node(str(i), self.aft_msa.entity_list[i][0], shape="circle")
                    else:
                        command.node(str(i), self.aft_msa.entity_list[i][0], shape="doublecircle")

                    command.node(str(i) + "a", self.aft_msa.entity_list[i][1], shape="none")
                    command.edge("R", str(i), arrowType="none")
                    command.edge(str(i), str(i)+"a", style="invis")

                self.send_dot_telegram(command, update, context)
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")
                update.message.reply_text("Type name of Entity")

    def print_coupling_dot_LR(self, update, context):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                self.selected = update.message.text
                self.load_entity(self.selected)
                command = Digraph(comment=self.entity.entity_name)
                command.attr(rankdir='LR')
                command.node('externalIn', "External Input", shape="box", color="plum1")
                command.node('externalOut', "External Output", shape="box", color="skyblue")
                command.node('R', self.entity.entity_name, shape="box", style="bold")

                if self.aft_msa.entity_list is not None:
                    for item in self.aft_msa.entity_list:
                        if item[2]:
                            command.node(item[0], item[0], shape="box")
                        else:
                            command.node(item[0], item[0], shape="polygon")

                if self.aft_msa.external_input_map is not None:
                    i = 0
                    for keys, values in self.aft_msa.external_input_map.items():
                        command.node(keys+"exin"+str(i), keys, shape="rarrow", style='filled', color='plum1')
                        j = 0
                        for item in values:
                            command.node(keys+item[1]+"in"+str(j), item[1], shape="rarrow")
                            command.edge(keys+"exin"+str(i), keys+item[1]+"in"+str(j))
                            command.edge(keys+item[1]+"in"+str(j), item[0], style="dotted")
                            j += 1
                        i += 1

                if self.aft_msa.internal_coupling_map_tuple is not None:
                    i = 0
                    for keys, values in self.aft_msa.internal_coupling_map_tuple.items():
                        command.node(keys[1] + "internalOut"+str(i), keys[1], shape="rarrow")
                        j = 0
                        for item in values:
                            command.node(keys[1] + item[1] +"internalIn"+str(i)+str(j), item[1], shape="rarrow")
                            command.edge(keys[0], keys[1] + "internalOut"+str(i), style="dotted")
                            command.edge(keys[1] + "internalOut"+str(i), keys[1] + item[1] +"internalIn"+str(i)+str(j))
                            command.edge(keys[1] + item[1] +"internalIn"+str(i)+str(j), item[0], style="dotted")
                            j += 1
                        i += 1

                if self.aft_msa.external_output_map is not None:
                    i = 0
                    for keys, values in self.aft_msa.external_output_map.items():
                        command.node(keys+"exout"+str(i), keys, shape="rarrow", style='filled', color='skyblue')
                        j = 0
                        for item in values:
                            command.node(keys + item[1] + "out"+str(j), item[1], shape="rarrow")
                            command.edge(item[0], keys + item[1] + "out"+str(j), style="dotted")
                            command.edge(keys+item[1]+"out"+str(j), keys+"exout"+str(i))
                            j += 1
                        i += 1

                self.send_dot_telegram(command, update, context)
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")
                update.message.reply_text("Type name of Entity")

    def print_coupling_dot_UD(self, update, context):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                self.selected = update.message.text
                self.load_entity(self.selected)
                command = Digraph(comment=self.entity.entity_name)
                #command.node('externalIn', "External Input", shape="invhouse", color="red")
               # command.node('externalOut', "External Output", shape="invhouse", color="skyblue")
                #command.node('R', self.entity.entity_name, shape="box", style="bold")
                entity_height = "1.5"
                entity_width = "1.5"
                entity_fontsize = "30"
                port_height = "0.5"
                port_width = "0.5"
                port_fontsize = "1.5"

                if self.aft_msa.entity_list is not None:
                    for item in self.aft_msa.entity_list:
                        if item[2]:
                            command.node(item[0], item[0], shape="box", style="bold", height=entity_height,
                                         width=entity_width, fontsize=entity_fontsize)
                        else:
                            command.node(item[0], item[0], shape="box", style="bold", height=entity_height,
                                         width=entity_width, fontsize=entity_fontsize)

                if self.aft_msa.external_input_map is not None:
                    i = 0
                    for keys, values in self.aft_msa.external_input_map.items():
                        command.node(keys+"exin"+str(i), keys, shape="invhouse",
                                     style='filled', color='plum1', height=port_height, width=port_width)
                        j = 0
                        for item in values:
                            command.node(keys+item[1]+"in"+str(j), item[1], shape="invhouse", height=port_height,
                                         width=port_width)
                            command.edge(keys+"exin"+str(i), keys+item[1]+"in"+str(j))
                            command.edge(keys+item[1]+"in"+str(j), item[0], style="dotted")
                            j += 1
                        i += 1

                if self.aft_msa.internal_coupling_map_tuple is not None:
                    i = 0
                    for keys, values in self.aft_msa.internal_coupling_map_tuple.items():
                        command.node(keys[1] + "internalOut"+str(i), keys[1], shape="invhouse", height=port_height,
                                     width=port_width)
                        j = 0
                        for item in values:
                            command.node(keys[1] + item[1] +"internalIn"+str(i)+str(j), item[1], shape="invhouse",
                                         height=port_height, width=port_width)
                            command.edge(keys[0], keys[1] + "internalOut"+str(i), style="dotted")
                            command.edge(keys[1] + "internalOut"+str(i), keys[1] + item[1] +"internalIn"+str(i)+str(j))
                            command.edge(keys[1] + item[1] +"internalIn"+str(i)+str(j), item[0], style="dotted")
                            j += 1
                        i += 1

                if self.aft_msa.external_output_map is not None:
                    i = 0
                    for keys, values in self.aft_msa.external_output_map.items():
                        command.node(keys+"exout"+str(i), keys, shape="invhouse", style='filled', color='skyblue',
                                     height=port_height, width=port_width)
                        j = 0
                        for item in values:
                            command.node(keys + item[1] + "out"+str(j), item[1], shape="invhouse",
                                         height=port_height, width=port_width)
                            command.edge(item[0], keys + item[1] + "out"+str(j), style="dotted")
                            command.edge(keys+item[1]+"out"+str(j), keys+"exout"+str(i))
                            j += 1
                        i += 1

                self.send_dot_telegram(command, update, context)
                self.clear_system()
            else:
                update.message.reply_text("[ERR] Entity Not Found")
                update.message.reply_text("Type name of Entity")
