from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *

import dill

class Gen(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _item):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("GEN")
        self.insert_state("GEN", 1)
        self.insert_state("WAIT", "inf")

        self.insert_output_port("task")

        self.cur_item = 0
        self.gen_item = _item

    def ext_trans(self,port, msg):
        pass

    def output(self):
        msg = SysMessage(self.get_name(), "task")
        msg.insert(self.cur_item)
        msg.insert("gen")
        self.cur_item = self.cur_item + 1

        return msg

    def int_trans(self):
        if self.cur_item > self.gen_item:
            self._cur_state = "WAIT"

    @staticmethod
    def duplicate(instance_time, destruct_time, name, engine_name, _item):
        return Gen(instance_time, destruct_time, name, engine_name, _item)

class MsgRouter(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, _buf_cnt):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", "inf")
        self.insert_state("PROCESS", 0)

        self.insert_input_port("task_in")
        for i in range(_buf_cnt):
            self.insert_output_port("task_out[{0}]".format(i))

        self.buf_cnt = _buf_cnt
        self.cur_buf = 0
        self.msg_lst = None

    def ext_trans(self, port, msg):
        if port == "task_in":
            self.msg_lst = msg
            self._cur_state = "PROCESS"
        pass

    def output(self):
        if self._cur_state == "PROCESS":

            if self.cur_buf > self.buf_cnt:
                self.cur_buf = 0
            else:
                self.cur_buf = self.cur_buf + 1

            msg = SysMessage(self.get_name(), "task_out[{0}]".format(self.cur_buf))
            msg.insert(self.msg_lst.retrieve()[0])
            msg.insert(self.msg_lst.retrieve()[1])
#            msg.insert(self.msg_lst[1] + "->" + self.get_name())

            return msg
        else:
            return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

    @staticmethod
    def duplicate(instance_time, destruct_time, name, engine_name, _buf_cnt):
        return MsgRouter(instance_time, destruct_time, name, engine_name, _buf_cnt)

class Buf(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", "inf")
        self.insert_state("PROCESS", 0)

        self.insert_input_port("task_in")
        self.insert_output_port("task_out")

        self.msg_lst = None

    def ext_trans(self, port, msg):
        if port == "task_in":
            self.msg_lst = msg
            self._cur_state = "PROCESS"
        pass

    def output(self):
        if self._cur_state == "PROCESS":
            msg = SysMessage(self.get_name(), "task_out")
            msg.insert(self.msg_lst.retrieve()[0])
            msg.insert(self.msg_lst.retrieve()[1] + "->" + self.get_name())

            return msg
        else:
            return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

    @staticmethod
    def duplicate(instance_time, destruct_time, name, engine_name):
        return Buf(instance_time, destruct_time, name, engine_name)

class Proc(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", "inf")

        self.insert_input_port("task_in")

    def ext_trans(self, port, msg):
        if port == "task_in":
#            self.msg_lst = msg
            print("MSG_ID:{0}, Path: {1}".format(msg.retrieve()[0], msg.retrieve()[1]))
        pass

    def output(self):
        pass

    def int_trans(self):
        pass

    @staticmethod
    def duplicate(instance_time, destruct_time, name, engine_name):
        return Proc(instance_time, destruct_time, name, engine_name)

with open('./sample/EchoProtocol/Gen.sim', 'wb') as f:
    dill.dump(Gen(0, 10000, "Gen", "sname", 100), f)

with open('./sample/EchoProtocol/Router.sim', 'wb') as f:
    dill.dump(MsgRouter(0, 10000, "MsgRouter", "sname", 3), f)

with open('./sample/EchoProtocol/Buf.sim', 'wb') as f:
    dill.dump(Buf(0, 10000, "Buf", "sname"), f)

with open('./sample/EchoProtocol/Proc.sim', 'wb') as f:
    dill.dump(Proc(0, 10000, "Buf", "sname"), f)

g = None
r = None
b = None
p = None

with open('./sample/EchoProtocol/Gen.sim', 'rb') as f:
    g = dill.load(f)

with open('./sample/EchoProtocol/Router.sim', 'rb') as f:
    r = dill.load(f)

with open('./sample/EchoProtocol/Buf.sim', 'rb') as f:
    b = dill.load(f)

with open('./sample/EchoProtocol/Proc.sim', 'rb') as f:
    p = dill.load(f)

#se = SystemSimulator()

SystemSimulator().register_engine("sname")

ng = g.duplicate(0, 10000, "Gen", "sname", 100)
SystemSimulator().get_engine("sname").register_entity(ng)

nr = r.duplicate(0, 10000, "MsgRouter", "sname", 3)
SystemSimulator().get_engine("sname").register_entity(nr)

SystemSimulator().get_engine("sname").coupling_relation(ng, "task", nr, "task_in")

np = p.duplicate(0, 10000, "MsgRouter", "sname")
SystemSimulator().get_engine("sname").register_entity(np)

for i in range(3):
    nb = b.duplicate(0, 10000, "Buf[{0}]".format(i), "sname")
    SystemSimulator().get_engine("sname").register_entity(nb)
    SystemSimulator().get_engine("sname").coupling_relation(nr, "task_out[{0}]".format(i), nb, "task_in")
    SystemSimulator().get_engine("sname").coupling_relation(nb, "task_out", np, "task_in")

SystemSimulator().get_engine("sname").simulate()