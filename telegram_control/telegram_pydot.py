import pydot
from system_manager.system_manager import *
from io import BytesIO, StringIO
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

    def print_entity_dot(self, update, context):
        if self.operation_count == 0:
            self.print_entity_db(update)
            update.message.reply_text("Type name of Entity")
            self.operation_count += 1
        elif self.operation_count == 1:
            if update.message.text in self.model_db.keys():
                self.selected = update.message.text
                model = self.sm.esm.import_system_entity_structure(self.model_db[self.selected])
                self.load_entity(self.selected)
                command = Digraph(comment=self.entity.entity_name)
                command.node('R', self.entity.entity_name)
                edge_lst = []
                for i in range(len(self.aft_msa.entity_list)):
                    command.node(str(i), self.aft_msa.entity_list[i][0])
                    _str = "R"
                    _str += str(i)
                    edge_lst.append(_str)
                print(edge_lst)
                command.edges(edge_lst)

                '''
                command.edge('hello','world')
                command.node('A', 'Hello')
                command.node('B', 'World')
                command.edges(['AB'])
                print(type(command))
                '''
                command.format = 'png'
                ABC = command.render(view=False)
                img = Image.open(ABC)
                img = img.convert('RGB')
                bio = BytesIO()
                bio.name = 'image.jpeg'
                img.save(bio, 'JPEG')
                bio.seek(0)
                context.bot.send_photo(chat_id=update.message.chat_id, photo=bio)
                self.clear_system()