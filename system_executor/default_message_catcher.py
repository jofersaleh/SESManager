# from system_executor.system_simulator import *
from system_executor.behavior_model_executor import *
from system_executor.system_message import *


class DefaultMessageCatcher(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)

        self.insert_input_port("uncaught")

    def ext_trans(self, port, msg):
        data = msg.retrieve()

    def time_advance(self):
        return Infinite
