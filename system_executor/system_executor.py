"""
    Light-weighted Simulation Engine
"""

import datetime
from collections import deque
from system_executor.default_message_catcher import *


class SysExecutor(object):

    EXTERNAL_SRC = "SRC"
    EXTERNAL_DST = "DST"

    def __init__(self, time_step=1):
        self.global_time = 0
        self.time_step = time_step

        # dictionary for waiting simulation objects
        self.waiting_obj_map = {}
        # dictionary for active simulation objects
        self.active_obj_map = {}
        # dictionary for object to ports
        self.port_map = {}
        self.port_map_wName = []

        self.min_schedule_item = deque()

        self.sim_init_time = datetime.datetime.now()

        self.mode = "Simulation"
        self.eval_time = 0

        self.register_entity(DefaultMessageCatcher(0, Infinite, "dc", "default"))

    # retrieve global time
    def get_global_time(self):
        return self.global_time

    def register_entity(self, sim_obj):
        if not sim_obj.get_create_time() in self.waiting_obj_map:
            self.waiting_obj_map[sim_obj.get_create_time()] = list()

        self.waiting_obj_map[sim_obj.get_create_time()].append(sim_obj)

    def create_entity(self):
        if len(self.waiting_obj_map.keys()) != 0:
            key = min(self.waiting_obj_map)
            if key <= self.global_time:
                lst = self.waiting_obj_map[key]
                for obj in lst:
                    # print("global:",self.global_time," create agent:", obj.get_obj_name())
                    self.active_obj_map[obj.get_name()] = obj
                    # self.min_schedule_item.append((obj.time_advance() + self.global_time, obj))
                    obj.set_req_time(self.global_time)
                    self.min_schedule_item.append(obj)
                del self.waiting_obj_map[key]

                # select object that requested minimum time
                self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))

    def destroy_entity(self):
        if len(self.active_obj_map.keys()) != 0:
            delete_lst = []
            for agent_name, agent in self.active_obj_map.items():
                if agent.get_destruct_time() <= self.global_time:
                    delete_lst.append(agent)

            for agent in delete_lst:
                # print("global:",self.global_time," del agent:", agent.get_obj_name())
                del(self.active_obj_map[agent.get_name()])
                self.min_schedule_item.remove(agent)

    def coupling_relation(self, src_obj, out_port, dst_obj, in_port):
        self.port_map[(src_obj, out_port)] = (dst_obj, in_port)
        self.port_map_wName.append((src_obj.get_name(), out_port, dst_obj.get_name(), in_port))

    def update_coupling_relation(self):
        self.port_map.clear()

        for i in range(len(self.port_map_wName)):
            src_obj_name = self.port_map_wName[i][0]
            src_obj = None
            # find loaded obj with name
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == src_obj_name:
                    src_obj = self.min_schedule_item[q]
            out_port = self.port_map_wName[i][1]
            dst_obj_name = self.port_map_wName[i][2]
            dst_obj = None
            for q in range(len(self.min_schedule_item)):
                if self.min_schedule_item[q].get_name() == dst_obj_name:
                    dst_obj = self.min_schedule_item[q]
            in_port = self.port_map_wName[i][3]
            self.port_map[(src_obj, out_port)] = (dst_obj, in_port)

    def output_handling(self, obj, msg):
        if msg is not None:
            if (obj, msg.get_dst()) not in self.port_map:
                self.port_map[(obj, msg.get_dst())] = (self.active_obj_map["dc"], "uncaught")

            destination = self.port_map[(obj, msg.get_dst())]
            if destination is None:
                print("Destination Not Found")
                raise AssertionError

            # Receiver Message Handling
            destination[0].ext_trans(destination[1], msg)
            # Receiver Scheduling
            # wrong : destination[0].set_req_time(self.global_time + destination[0].time_advance())
            destination[0].set_req_time(self.global_time)
            # self.min_schedule_item.pop()
            # self.min_schedule_item.append((destination[0].time_advance() + self.global_time, destination[0]))

    def set_eval_time(self, time):
        self.eval_time = time

    def init_sim(self):
        self.global_time = min(self.waiting_obj_map)
        for obj in self.active_obj_map.items():
            if obj[1].time_advance() < 0: # exception handling for parent instance
                print("You should override the time_advanced function")
                raise AssertionError

            obj.set_req_time(self.global_time)
            self.min_schedule_item.append(obj)

    def schedule(self):
        # Agent Creation
        self.create_entity()

        tuple_obj = self.min_schedule_item.popleft()

        while tuple_obj.get_req_time() <= self.global_time:
            msg = tuple_obj.output()
            if msg is not None:
                self.output_handling(tuple_obj, msg)

            # Sender Scheduling
            tuple_obj.int_trans()
            tuple_obj.set_req_time(self.global_time)
            self.min_schedule_item.append(tuple_obj)

            self.min_schedule_item = deque(sorted(self.min_schedule_item, key=lambda bm: bm.get_req_time()))
            tuple_obj = self.min_schedule_item.popleft()

        self.min_schedule_item.appendleft(tuple_obj)

        # update Global Time
        self.global_time += self.time_step

        # Agent Deletion
        self.destroy_entity()

    def simulate(self):
        self.init_sim()
        while True:
            if not self.waiting_obj_map:
                if self.min_schedule_item[0].get_req_time() == Infinite:
                    break

            self.schedule()
