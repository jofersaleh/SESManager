from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import math

class Agent5(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.x = 0
        self.y = 0
        self.waypoints = [(10,10), (20,20), (30,30), (30,0), (0, 0)]
        print("waypoint: ", self.waypoints)


        self.init_state("IDLE")
        self.insert_state("IDLE", 0)
        self.insert_state("WAIT", 0)
        self.insert_state("SEND", 1)
        self.insert_state("REACHED", 1)

        self.insert_input_port("received")
        self.insert_output_port("waypoint")



    def check_done(self):
        print("1")
        if not self.waypoints:
            return True
        else:
            return False


    def ext_trans(self,port, msg):
        print("2")
        if port == "received":
            self._cur_state = "SEND"
        else:
            data = msg.retrieve()
            print(data[0])

    def output(self):
        print("5")
        self._cur_state = "WAIT"
        location = self.waypoints[0]
        print(location)
        msg = SysMessage(self.get_name(), location)
        print("6")
        return msg

    def int_trans(self):
        print("4")
        if self._cur_state == "IDLE":
            print("7")
            self._cur_state = "SEND"
        if self.waypoints is None:
            self._cur_state = "REACHED"



class Maneuver(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("IDLE")
        self.insert_state("IDLE", 0)
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

    def output(self):
        if self._cur_state == "FINISH":
            msg = self.result
            self.result = []
            self._cur_state = "IDLE"
            return msg

    def int_trans(self):
        self.move()


h = Agent5(0, 100, "Peter", "sname")
r = Maneuver(0, 100, "Simon", "sname")

with open('./sample/model_db/Gen5.pkl', 'wb') as f:
    dill.dump(Agent5(0, 100, "Peter", "sname"), f)
with open('./sample/model_db/Maneuver.pkl', 'wb') as f:
    dill.dump(Maneuver(0, 100, "Simon", "sname"), f)

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

SystemSimulator().get_engine("sname").register_entity(h)
SystemSimulator().get_engine("sname").register_entity(r)
SystemSimulator().get_engine("sname").coupling_relation(h, "waypoint", r, "recv")
SystemSimulator().get_engine("sname").coupling_relation(r, "send_result", h, "received")
SystemSimulator().get_engine("sname").simulate()