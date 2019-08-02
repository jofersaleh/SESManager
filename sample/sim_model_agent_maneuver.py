from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import math
from random import uniform

class Agent5(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.waypoints = [(uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100))]
        print("waypoint: ", self.waypoints)
        self.result = []


        self.init_state("IDLE")
        self.insert_state("IDLE", 0)
        self.insert_state("WAIT", 0)
        self.insert_state("SEND", 1)
        self.insert_state("REACHED", 1)

        self.insert_input_port("exin")
        self.insert_input_port("received")
        self.insert_output_port("waypoint")
        self.insert_output_port("exout")



    def check_done(self):
        print("1")
        if not self.waypoints:
            return True
        else:
            return False


    def ext_trans(self,port, msg):
        print("2")
        if port == "exin":
            print("3")
            self._cur_state = "SEND"
        elif port == "received":
            if self.check_done():
                data = msg.retrieve()
                self.result.append(data[0])
                self._cur_state = "SEND"
            else:
                self._cur_state = "REACHED"
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        if self._cur_state == "SEND":
            self._cur_state = "WAIT"
            location = self.waypoints[0]
            print(location)
            msg = SysMessage(self.get_name(), location)
            print("6")
            return msg
        elif self._cur_state == "REACHED":
            msg = SysMessage(self.get_name(), self.result)
            print("99")
            return msg

    def int_trans(self):
        if self._cur_state == "IDLE":
            print("7")
            self._cur_state = "SEND"
            self.output()
        if self.waypoints is None:
            self._cur_state = "REACHED"



class Maneuver(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("LISTEN")
        self.insert_state("LISTEN", 0)
        self.insert_state("MOVE", 1)
        self.insert_state("FINSH", 1)

        self.waypoint = None
        self.result = []

        self.pos = [0,0]
        self.vel = 1

        self.insert_input_port("recv")
        self.insert_output_port("send_result")

    def check_reached(self, pos0, pos1, error):
        if math.sqrt(math.pow(pos0[0] - pos1[0], 2) + math.pow(pos0[1] - pos1[1], 2)) < error:
            return True
        else:
            return False

    def move(self):
        if self.waypoint is not None:
            way_x, way_y = self.waypoint
            rad = math.atan2((way_y - self.pos[1]), (way_x - self.pos[0]))
            self.pos[0] += self.vel * math.cos(rad)
            self.pos[1] += self.vel * math.sin(rad)

            if self.check_reached(self.waypoint, self.pos, 1):
                self._cur_state = "FINISH"
                self.waypoint = None
        else:
            self._cur_state = "IDLE"

    def ext_trans(self, port, msg):
        print("11")
        data = msg.retrieve()
        self.waypoint = data[0]
        self._cur_state = "MOVE"
        self.move()

    def output(self):
        if self._cur_state == "FINISH":
            msg = self.result
            self.result = []
            self._cur_state = "IDLE"
            return msg

    def int_trans(self):
        #print("77")
        if self._cur_state == "MOVE":
            print("88")
            self.move()




h = Agent5(0, 1000, "Peter", "sname")
r = Maneuver(0, 1000, "Simon", "sname")

with open('./sample/model_db/Gen5.pkl', 'wb') as f:
    dill.dump(Agent5(0, 1000, "Peter", "sname"), f)
with open('./sample/model_db/Maneuver.pkl', 'wb') as f:
    dill.dump(Maneuver(0, 1000, "Simon", "sname"), f)

h = None
r = None

with open('./sample/model_db/Gen5.pkl', 'rb') as f:
    h = dill.load(f)

with open('./sample/model_db/Maneuver.pkl', 'rb') as f:
    r = dill.load(f)

#se = SystemSimulator()

SystemSimulator().register_engine("sname")
#print("!")
#print(SystemSimulator.get_engine("sname"))

SystemSimulator().get_engine("sname").insert_input_port("in")
SystemSimulator().get_engine("sname").register_entity(h)
SystemSimulator().get_engine("sname").register_entity(r)
SystemSimulator().get_engine("sname").coupling_relation(None, "in", h, "exin")
SystemSimulator().get_engine("sname").coupling_relation(h, "exout", None, "out")
SystemSimulator().get_engine("sname").coupling_relation(h, "waypoint", r, "recv")
SystemSimulator().get_engine("sname").coupling_relation(r, "send_result", h, "received")
SystemSimulator().get_engine("sname").insert_external_event("in", None)
SystemSimulator().get_engine("sname").simulate()
print(SystemSimulator().get_engine("sname").handle_external_output_event())