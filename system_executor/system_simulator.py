from system_executor.system_executor import *


class SingletonType(object):
    def __call__(self, cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class SystemSimulator(object):
    __metaclass__ = SingletonType
    _engine = {}

    @staticmethod
    def register_engine(sim_name, time_step=1):
        SystemSimulator._engine[sim_name] = SysExecutor(time_step)

    @staticmethod
    def get_engine_map():
        return SystemSimulator._engine

    @staticmethod
    def get_engine(sim_name):
        return SystemSimulator._engine[sim_name]

    def __init__(self):
        pass
