from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *


class Grace(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("Feature", 0)
        self.insert_state("Location", 0)

        self.insert_input_port("asked feature")
        self.insert_input_port("asked location")
        self.insert_output_port("answer")

    def ext_trans(self, port, msg):
        if port == "asked feature":
            self._cur_state = "Feature"
            print("[{}]{}Event received from external".format(datetime.datetime.now(), self.get_name()))
        elif port == "asked location":
            self._cur_state = "Location"
            print("[{}]{}Event received from external".format(datetime.datetime.now(), self.get_name()))
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        print("Grace!")
        if self._cur_state == "Feature":
            msg = SysMessage(self.get_name(), "answer")
            print(str(datetime.datetime.now()) + " Grace feature:")
            msg.insert("Domi")
            return msg
        elif self._cur_state == "Location":
            msg = SysMessage(self.get_name(), "answer")
            print(str(datetime.datetime.now()) + " Grace location:")
            msg.insert("left corner")
            return msg

    def int_trans(self):
        if self._cur_state == "Feature":
            self._cur_state = "IDLE"
        elif self._cur_state == "Location":
            self._cur_state = "IDLE"


class Evenecel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("Feature", 0)
        self.insert_state("Location", 0)

        self.insert_input_port("asked feature")
        self.insert_input_port("asked location")
        self.insert_output_port("answer")

    def ext_trans(self, port, msg):
        if port == "asked feature":
            self._cur_state = "Feature"
            print("[{}]{}Event received from external".format(datetime.datetime.now(), self.get_name()))

        elif port == "asked location":
            self._cur_state = "Location"
            print("[{}]{}Event received from external".format(datetime.datetime.now(), self.get_name()))
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        print("Evenecel!")
        if self._cur_state == "Feature":
            msg = SysMessage(self.get_name(), "answer")
            print(str(datetime.datetime.now()) + " Evenecel feature:")
            msg.insert("Class")
            return msg
        elif self._cur_state == "Location":
            msg = SysMessage(self.get_name(), "answer")
            print(str(datetime.datetime.now()) + " Evenecel location:")
            msg.insert("Right corner")
            return msg

    def int_trans(self):
        if self._cur_state == "Feature":
            self._cur_state = "IDLE"
        elif self._cur_state == "Location":
            self._cur_state = "IDLE"


class Display(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("MOVE")
        self.insert_state("MOVE", Infinite)

        self.insert_state("Action", 0)

        self.insert_input_port("get information")
        self.insert_output_port("information out")

    def ext_trans(self, port, msg):
        data = msg.retrieve()
        print(data)
        if self._cur_state == "MOVE":
            self._cur_state = "Action"
            print("[{0:05}] {1} {2}".format(SystemSimulator().get_engine(self.engine_name).get_global_time(), str(datetime.datetime.now()), str(data[0])))
        else:
            self._cur_state = "Action"
            print("[{0:05}] {1} {2}".format(SystemSimulator().get_engine(self.engine_name).get_global_time(),
                                            str(datetime.datetime.now()), str(data[0])))

    def output(self):
        print("####")
        if self._cur_state == "Action":
            msg = SysMessage(self.get_name(), "information out")
            return msg
        else:
            return None

    def int_trans(self):
        if self._cur_state == "Action":
            self._cur_state = "MOVE"


grace = Grace(0, 10, "Grace", "sname")
evenecel = Evenecel(0, 10, "Evenecel", "snmae")
display = Display(0, 10, "Display", "sname")

#se = SystemSimulator()

SystemSimulator().register_engine("sname")
#print("!")
#print(SystemSimulator.get_engine("sname"))

SystemSimulator().get_engine("sname").insert_input_port("feature")
SystemSimulator().get_engine("sname").insert_input_port("location")

SystemSimulator().get_engine("sname").insert_output_port("displayed")

SystemSimulator().get_engine("sname").register_entity(grace)
SystemSimulator().get_engine("sname").register_entity(evenecel)
SystemSimulator().get_engine("sname").register_entity(display)
SystemSimulator().get_engine("sname").coupling_relation(None, "feature", grace, "asked feature")
SystemSimulator().get_engine("sname").coupling_relation(grace, "answer", display, "get information")
SystemSimulator().get_engine("sname").coupling_relation(display, "information out", None, "displayed")

SystemSimulator().get_engine("sname").coupling_relation(None, "feature", evenecel, "asked feature")
SystemSimulator().get_engine("sname").coupling_relation(evenecel, "answer", display, "get information")
SystemSimulator().get_engine("sname").coupling_relation(display, "information out", None, "displayed")

SystemSimulator().get_engine("sname").insert_external_event("feature", None)
SystemSimulator().get_engine("sname").simulate(10)
print(1)
SystemSimulator().get_engine("sname").coupling_relation(None, "location", grace, "asked location")
SystemSimulator().get_engine("sname").coupling_relation(grace, "answer", display, "get information")
SystemSimulator().get_engine("sname").coupling_relation(display, "information out", None, "displayed")
SystemSimulator().get_engine("sname").insert_external_event("location", None)
SystemSimulator().get_engine("sname").simulate(10)
print(1)
'''
print(2)
print(SystemSimulator().get_engine("sname").handle_external_output_event())

while not SystemSimulator().get_engine("sname").is_terminated():
    SystemSimulator().get_engine("sname").simulate(1)
'''

