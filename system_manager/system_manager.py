from system_manager.es_manager import *
from model_base.modelmanager import *
from system_manager.execution_manager import *


class SystemManager(object):
    def __init__(self, _edb, _mdb, _pdb):
        self.esm = EntityManager(_edb)
        self.mm = ModelManager(_mdb)
        self.em = ExecutionManager(_pdb, _mdb)
        pass

    @staticmethod
    def menu():
        print("System Management System")
        print("1. Entity Management")
        print("2. Model Management")
        print("3. Model Synthesis")
        print("4. Execution Management")
        print("0. Exit")
        return int(input(">>"))

    def start(self):
        loop = True
        while loop:
            selected = SystemManager.menu()

            if selected == 1:
                self.esm.start()
                pass
            elif selected == 2:
                # TODO Implement
                pass
            elif selected == 3:
                self.esm.interactive_pruning()
                pass
            elif selected == 4:
                self.em.start()
                pass
            else:
                loop = False
