from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import dill


class Human(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.spd = 10

        self.init_state("IDLE")
        self.insert_state("IDLE", 0)
        self.insert_state("MOVE", 1)

        self.insert_input_port("greeting")
        self.insert_output_port("hello")

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        print(data[0])

    def output(self):
        self.x += self.spd
        self.y += self.spd

        #temp = "[%f] (%d, %d)" % (SystemSimulator().get_engine(self.engine_name).get_global_time(), self.x, self.y)
        #print(temp)
        msg = SysMessage(self.get_name(), "hello")
        print(str(datetime.datetime.now()) + " Human Object:")
        msg.insert("I am")
        return msg

    def int_trans(self):
        if self._cur_state == "IDLE":
            self._cur_state = "MOVE"
        else:
            self._cur_state = "MOVE"


class Receiver(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.x = 0
        self.y = 0
        self.spd = 10

        self.init_state("MOVE")
        self.insert_state("MOVE", 1)

        self.insert_input_port("greeting")

    def ext_trans(self,port, msg):
        data = msg.retrieve()
        print(str(datetime.datetime.now()) +  " " + str(data[0]))
        #temp = "[%f] %s" % (SystemSimulator().get_engine(self.engine_name).get_global_time(), str(data[0]))
        #print(temp)

    def output(self):
        #temp = "[%f] %s" % (SystemSimulator().get_engine(self.engine_name).get_global_time(), "Human Receiver Object: Move")
        #print(temp)
        return None

    def int_trans(self):
        self._cur_state = "MOVE"


with open('./sample/model_db/Human.pkl', 'wb') as f:
    dill.dump(Human(0, 100, "Peter", "sname"), f)

with open('./sample/model_db/Receiver.pkl', 'wb') as f:
    dill.dump(Receiver(0, 100, "Simon", "sname"), f)

h = None
r = None

with open('./sample/model_db/Human.pkl', 'rb') as f:
    h = dill.load(f)

with open('./sample/model_db/Receiver.pkl', 'rb') as f:
    r = dill.load(f)

#se = SystemSimulator()

SystemSimulator().register_engine("sname")
#print("!")
#print(SystemSimulator.get_engine("sname"))

SystemSimulator().get_engine("sname").register_entity(h)
SystemSimulator().get_engine("sname").register_entity(r)
SystemSimulator().get_engine("sname").coupling_relation(h, "hello", r, "greeting")
SystemSimulator().get_engine("sname").simulate()