from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import math
from random import uniform


class Agent5(BehaviorModelExecutor):
    #import copy
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.waypoints = [(uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100))]
        print("waypoint Agent5: ", self.waypoints)
        self.result = []

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WAIT", Infinite)
        self.insert_state("SEND", 0)
        self.insert_state("REACHED", 0)

        self.insert_input_port("exin")
        self.insert_input_port("received")
        self.insert_output_port("waypoint")
        self.insert_output_port("exout")



    def check_done(self):
        if self.waypoints == []:
            return False
        else:
            return True

    def ext_trans(self,port, msg):
        if port == "exin":
            self._cur_state = "SEND"
        elif port == "received":
            data = msg.retrieve()
            self.result.append(copy.deepcopy(data[0]))
            if self.check_done():
                self._cur_state = "SEND"
            else:
                self._cur_state = "REACHED"
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        if self._cur_state == "SEND":
            location = self.waypoints.pop(0)
            msg = SysMessage(self.get_name(), "waypoint")
            msg.insert(location)
            return msg
        elif self._cur_state == "REACHED":
            msg = SysMessage(self.get_name(), "exout")
            msg.insert(self.result)
            return msg

    def int_trans(self):
        if self._cur_state == "SEND":
            self._cur_state = "WAIT"
        if self.waypoints is None:
            self._cur_state = "REACHED"
        if self._cur_state == "REACHED":
            self._cur_state = "IDLE"



class Agent10(BehaviorModelExecutor):
    #import copy
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.waypoints = [(uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100))
                          ]
        print("waypoint Agent10: ", self.waypoints)
        self.result = []

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WAIT", Infinite)
        self.insert_state("SEND", 0)
        self.insert_state("REACHED", 0)

        self.insert_input_port("exin")
        self.insert_input_port("received")
        self.insert_output_port("waypoint")
        self.insert_output_port("exout")



    def check_done(self):
        if self.waypoints == []:
            return False
        else:
            return True

    def ext_trans(self,port, msg):
        if port == "exin":
            self._cur_state = "SEND"
        elif port == "received":
            data = msg.retrieve()
            self.result.append(copy.deepcopy(data[0]))
            if self.check_done():
                self._cur_state = "SEND"
            else:
                self._cur_state = "REACHED"
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        if self._cur_state == "SEND":
            location = self.waypoints.pop(0)
            msg = SysMessage(self.get_name(), "waypoint")
            msg.insert(location)
            return msg
        elif self._cur_state == "REACHED":
            msg = SysMessage(self.get_name(), "exout")
            msg.insert(self.result)
            return msg

    def int_trans(self):
        if self._cur_state == "SEND":
            self._cur_state = "WAIT"
        if self.waypoints is None:
            self._cur_state = "REACHED"
        if self._cur_state == "REACHED":
            self._cur_state = "IDLE"

class Agent20(BehaviorModelExecutor):
    #import copy
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.waypoints = [(uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)), (uniform(0,100), uniform(0,100)),
                          (uniform(0,100), uniform(0,100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100)), (uniform(0, 100), uniform(0, 100)),
                          (uniform(0, 100), uniform(0, 100))
                          ]
        print("waypoint Agent20: ", self.waypoints)
        self.result = []

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("WAIT", Infinite)
        self.insert_state("SEND", 0)
        self.insert_state("REACHED", 0)

        self.insert_input_port("exin")
        self.insert_input_port("received")
        self.insert_output_port("waypoint")
        self.insert_output_port("exout")



    def check_done(self):
        if self.waypoints == []:
            return False
        else:
            return True

    def ext_trans(self,port, msg):
        if port == "exin":
            self._cur_state = "SEND"
        elif port == "received":
            data = msg.retrieve()
            self.result.append(copy.deepcopy(data[0]))
            if self.check_done():
                self._cur_state = "SEND"
            else:
                self._cur_state = "REACHED"
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        if self._cur_state == "SEND":
            location = self.waypoints.pop(0)
            msg = SysMessage(self.get_name(), "waypoint")
            msg.insert(location)
            return msg
        elif self._cur_state == "REACHED":
            msg = SysMessage(self.get_name(), "exout")
            msg.insert(self.result)
            return msg

    def int_trans(self):
        if self._cur_state == "SEND":
            self._cur_state = "WAIT"
        if self.waypoints is None:
            self._cur_state = "REACHED"
        if self._cur_state == "REACHED":
            self._cur_state = "IDLE"



class Maneuver(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("LISTEN")
        self.insert_state("LISTEN", Infinite)
        self.insert_state("MOVE", 1)
        self.insert_state("FINSH", 1)

        self.waypoint = None

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
        data = msg.retrieve()
        self.waypoint = data[0]
        self._cur_state = "MOVE"
        self.move()

    def output(self):
        if self._cur_state == "FINISH":
            msg = SysMessage(self.get_name(), "send_result")
            msg.insert(self.pos)
            self.result = []
            return msg

    def int_trans(self):
        if self._cur_state == "MOVE":
            self.move()
        else:
            self._cur_state = "LISTEN"




v = Agent5(0, 1000, "Peter", "sname")
x = Agent10(0, 10000, "Cheolsoo", "sname")
xx = Agent20(0, 10000, "Minsoo", "sname")
mv = Maneuver(0, 1000, "Simon", "sname")
mx = Maneuver(0, 10000, "Simon2", "sname")
mxx = Maneuver(0, 10000, "Simon3", "sname")

SystemSimulator().register_engine("sname")

SystemSimulator().get_engine("sname").insert_input_port("in")
SystemSimulator().get_engine("sname").insert_input_port("in2")
SystemSimulator().get_engine("sname").insert_input_port("in3")

SystemSimulator().get_engine("sname").register_entity(v)
SystemSimulator().get_engine("sname").register_entity(x)
SystemSimulator().get_engine("sname").register_entity(xx)
SystemSimulator().get_engine("sname").register_entity(mv)
SystemSimulator().get_engine("sname").register_entity(mx)
SystemSimulator().get_engine("sname").register_entity(mxx)

SystemSimulator().get_engine("sname").coupling_relation(None, "in", v, "exin")
SystemSimulator().get_engine("sname").coupling_relation(v, "exout", None, "out")
SystemSimulator().get_engine("sname").coupling_relation(v, "waypoint", mv, "recv")
SystemSimulator().get_engine("sname").coupling_relation(mv, "send_result", v, "received")

SystemSimulator().get_engine("sname").coupling_relation(None, "in2", x, "exin")
SystemSimulator().get_engine("sname").coupling_relation(x, "exout", None, "out")
SystemSimulator().get_engine("sname").coupling_relation(x, "waypoint", mx, "recv")
SystemSimulator().get_engine("sname").coupling_relation(mx, "send_result", x, "received")

SystemSimulator().get_engine("sname").coupling_relation(None, "in3", xx, "exin")
SystemSimulator().get_engine("sname").coupling_relation(xx, "exout", None, "out")
SystemSimulator().get_engine("sname").coupling_relation(xx, "waypoint", mxx, "recv")
SystemSimulator().get_engine("sname").coupling_relation(mxx, "send_result", xx, "received")

SystemSimulator().get_engine("sname").insert_external_event("in", None)
SystemSimulator().get_engine("sname").insert_external_event("in2", None)
SystemSimulator().get_engine("sname").insert_external_event("in3", None)
SystemSimulator().get_engine("sname").simulate()
print(SystemSimulator().get_engine("sname").handle_external_output_event())

