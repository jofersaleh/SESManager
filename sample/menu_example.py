from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import dill

class DisplayObject(object):
    def action(self):
        print("1. a")
        print("2. b")
        print("3. c")

        return None

class Display(BehaviorModelExecutor):
    def __init__(self, name, engine_name):
        BehaviorModelExecutor.__init__(self, 0, Infinite, name, engine_name)

        self.init_state("DISPLAY")
        self.insert_state("DISPLAY", 0)
        self.insert_state("WAIT", Infinite)

        self.insert_input_port("in")
        self.insert_output_port("out")

        self.domain_obj = None

    def ext_trans(self, port, msg):
        if port == "in":
            self._cur_state = "DISPLAY"

    def output(self):
        if self._cur_state == "DISPLAY":
            command = self.domain_obj.action()
            msg = SysMessage(self.get_name(), "out")
            msg.insert(command)
            return msg
        else:
            return None

    def int_trans(self):
        if self._cur_state == "DISPLAY":
            self._cur_state = "WAIT"
        else:
            self._cur_state = "WAIT"

class SelectionObject(object):
    def action(self):
        command = int(input(">>"))
        return command

class Selection(BehaviorModelExecutor):
    def __init__(self, name, engine_name):
        BehaviorModelExecutor.__init__(self, 0, Infinite, name, engine_name)

        self.init_state("WAIT")
        self.insert_state("SELECTION", 0)
        self.insert_state("WAIT", Infinite)

        self.insert_input_port("in")
        self.insert_output_port("out")

        self.domain_obj = None

    def ext_trans(self, port, msg):
        if port == "in":
            self._cur_state = "SELECTION"

    def output(self):
        if self._cur_state == "SELECTION":
            command = self.domain_obj.action()
            msg = SysMessage(self.get_name(), "out")
            msg.insert(command)
            return msg
        else:
            return None

    def int_trans(self):
        if self._cur_state == "SELECTION":
            self._cur_state = "WAIT"
        else:
            self._cur_state = "WAIT"

class ActionObject(object):
    def __init__(self):
        self.event_list = []
    def update_event(self, event_list):
        self.event_list = event_list

    def action(self):
        command = 0
        for event in self.event_list:
            if event == 1:
                print("!")
                command = 1
            elif event == 2:
                print("@@")
                command = 2
            elif event == 3:
                print("###")
                command = 3
            else:
                print("$$$$")
                command = None

        return command

class Action(BehaviorModelExecutor):
    def __init__(self, name, engine_name):
        BehaviorModelExecutor.__init__(self, 0, Infinite, name, engine_name)

        self.init_state("WAIT")
        self.insert_state("ACTION", 0)
        self.insert_state("WAIT", Infinite)

        self.insert_input_port("in")
        self.insert_output_port("out")

        self.domain_obj = None

    def ext_trans(self, port, msg):
        if port == "in":
            self.domain_obj.update_event(msg.retrieve())
            self._cur_state = "ACTION"

    def output(self):
        if self._cur_state == "ACTION":
            command = self.domain_obj.action()
            msg = SysMessage(self.get_name(), "out")
            if command is not None:
                msg.insert(command)
                return msg

        return None

    def int_trans(self):
        if self._cur_state == "ACTION":
            self._cur_state = "WAIT"
        else:
            self._cur_state = "WAIT"

d = Display("d", "tl")
with open('./sample/model_db/Display.pkl', 'wb') as f:
    dill.dump(d, f)

d.domain_obj = DisplayObject()
with open('./sample/domain_db/DisplayObject.pkl', 'wb') as f:
    dill.dump(d.domain_obj, f)

s = Selection("s", "tl")
with open('./sample/model_db/Selection.pkl', 'wb') as f:
    dill.dump(s, f)
s.domain_obj = SelectionObject()
with open('./sample/domain_db/SelectionObject.pkl', 'wb') as f:
    dill.dump(s.domain_obj, f)

a = Action("a", "tl")
with open('./sample/model_db/Action.pkl', 'wb') as f:
    dill.dump(a, f)
a.domain_obj = ActionObject()
with open('./sample/domain_db/ActionObject.pkl', 'wb') as f:
    dill.dump(a.domain_obj, f)

SystemSimulator().register_engine("tl")
SystemSimulator().get_engine("tl").register_entity(d)
SystemSimulator().get_engine("tl").register_entity(s)
SystemSimulator().get_engine("tl").register_entity(a)
SystemSimulator().get_engine("tl").coupling_relation(d, "out", s, "in")
SystemSimulator().get_engine("tl").coupling_relation(s, "out", a, "in")
SystemSimulator().get_engine("tl").coupling_relation(a, "out", d, "in")
SystemSimulator().get_engine("tl").simulate()
