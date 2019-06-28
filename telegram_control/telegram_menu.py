from telegram_control.telegram_es_manager import *
from telegram_control.telegram_execution_manager import *
from telegram_control.telegram_pydot import *
from telegram_control.telegram_synthesis import *

def check_operation(count):
    if count == 0:
        return True
    else:
        return False


class Remote_telegram:
    def __init__(self):
        self.STATUS = ""
        self.operation_TF = False
        self.es_manager = None
        self.dot_manager = None
        self.em_manager = None
        self.synthesis_manager = None

    def es_operation_start(self, update, context):
        print("!")
        self.es_manager = telegram_entityManager()
        self.setting_step(update, context)
        self.operation_TF = True

    def dot_operation_start(self, update, context):
        print("!")
        self.dot_manager = telegram_dotManager()
        self.setting_step(update, context)
        self.operation_TF = True

    def synthesis_operation_start(self, update, context):
        print("!")
        self.synthesis_manager = telegram_synthesisManager()
        self.setting_step(update, context)
        self.operation_TF = True


    def em_operation_start(self, update, context):
        print("!")
        self.em_manager = telegram_executionManager()
        self.setting_step(update, context)
        self.operation_TF = True

    def print_current_menu(self, update, context, current_num):
        print(self.STATUS)
        if current_num == 1:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. Create new Entity\n2. Read Entity\n"
                                          "3. Update Entity\n4. Delete Entity\n0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.es_operation_start(update, context)
                elif self.STATUS[0] == "2":
                    self.dot_operation_start(update, context)
                elif self.STATUS[0] == "3":
                    self.synthesis_operation_start(update, context)
                elif self.STATUS[0] == "4":
                    self.em_operation_start(update, context)
            elif len(self.STATUS) == 3:
                if self.STATUS[0:2] == "13":
                    self.es_operation_start(update, context)
            elif len(self.STATUS) == 4:
                if self.STATUS[0:3] == "133":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:3] == "134":
                    update.message.reply_text("What did you want to insert? \n 1. Input port\n2. Output port\n"
                                              "3. External input port\n4. External output port\n"
                                              "5. Internal port \n 0. Exit")
            elif len(self.STATUS) == 5:
                if self.STATUS[0:4] == "1341":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1342":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1343":
                    self.es_operation_start(update, context)
            else:
                update.message.reply_text("Please type again")
                self.STATUS = self.STATUS[:-1]

        elif current_num == 2:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. See entity by dot \n 2. See coupling by dot Left to Right \n"
                                          "3. See coupling by dot Up to Down \n 0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.es_operation_start(update, context)
                elif self.STATUS[0] == "2":
                    self.dot_operation_start(update, context)
                elif self.STATUS[0] == "3":
                    self.synthesis_operation_start(update, context)
                elif self.STATUS[0] == "4":
                    self.em_operation_start(update, context)
            elif len(self.STATUS) == 3:
                if self.STATUS[0:2] == "13":
                    self.es_operation_start(update, context)
            elif len(self.STATUS) == 4:
                if self.STATUS[0:3] == "133":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:3] == "134":
                    update.message.reply_text("What did you want to delete? \n 1. Input port\n2. Output port\n"
                                              "3. External input port\n4. External output port\n"
                                              "5. Internal port \n 0. Exit")
            elif len(self.STATUS) == 5:
                if self.STATUS[0:4] == "1341":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1342":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1343":
                    self.es_operation_start(update, context)

            else:
                update.message.reply_text("Please type again")
                self.STATUS = self.STATUS[:-1]

        elif current_num == 3:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. Interactive Pruning\n2.Print pruned entity\n3.Delete pruned entity\n"
                                          "4.Update pruned entity \n0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    update.message.reply_text("What did you want to modify entity\n1. Add Entity\n2. Delete Entity"
                                              "\n3. Modify inside of Entity\n4. Modify Port\n0. Exit")
                elif self.STATUS[0] == "2":
                    self.dot_operation_start(update, context)
                elif self.STATUS[0] == "3":
                    self.synthesis_operation_start(update, context)
                elif self.STATUS[0] == "4":
                    self.em_operation_start(update, context)
            elif len(self.STATUS) == 3:
                if self.STATUS[0:2] == "13":
                    update.message.reply_text("What did you want to modify? \n1. Name\n"
                                              "2. Attribute\n 3. optional\n0. Exit")
            elif len(self.STATUS) == 4:
                if self.STATUS[0:3] == "133":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:3] == "134":
                    update.message.reply_text("What did you want to change? \n 1. Input port\n2. Output port\n"
                                              "0. Exit")
            elif len(self.STATUS) == 5:
                if self.STATUS[0:4] == "1341":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1342":
                    self.es_operation_start(update, context)

            else:
                update.message.reply_text("Please type again")
                self.STATUS = self.STATUS[:-1]

        elif current_num == 4:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. List Pruned Entity Structure\n 2. Simulation Start\n"
                                          "3. Execute System\n 4. Synthesize Executable \n 0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.es_operation_start(update, context)
                elif self.STATUS[0] == "3":
                    self.synthesis_operation_start(update, context)
                elif self.STATUS[0] == "4":
                    self.em_operation_start(update, context)
            elif len(self.STATUS) == 3:
                if self.STATUS[0:2] == "13":
                    update.message.reply_text("What did you want to modify? \n1. Insert new port\n"
                                              "2. Delete port\n 3. Change name of port\n0. Exit")
            elif len(self.STATUS) == 5:
                if self.STATUS[0:4] == "1341":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1342":
                    self.es_operation_start(update, context)
        elif current_num == 5:
            if len(self.STATUS) == 5:
                if self.STATUS[0:4] == "1341":
                    self.es_operation_start(update, context)
                elif self.STATUS[0:4] == "1342":
                    self.es_operation_start(update, context)
            else:
                update.message.reply_text("Please type again")
                self.STATUS = self.STATUS[:-1]

    def setting_step(self, update, context):
        if self.STATUS[0] == "1":
            if len(self.STATUS) == 2:
                if self.STATUS == "11":
                    self.es_manager.create_option(update)
                elif self.STATUS == "12":
                    self.es_manager.read_option(update)
                elif self.STATUS == "14":
                    self.es_manager.delete_entity(update)
            elif len(self.STATUS) == 3:
                if self.STATUS == "131":
                    self.es_manager.update_option_addenti(update)
                elif self.STATUS == "132":
                    self.es_manager.update_option_deletenti(update)
            elif len(self.STATUS) == 4:
                if self.STATUS == "1331":
                    self.es_manager.update_option_modienti_name(update)
                elif self.STATUS == "1332":
                    self.es_manager.update_option_modienti_attribute(update)
                elif self.STATUS == "1333":
                    self.es_manager.update_option_modienti_optional(update)
            else:
                if self.STATUS[3] == "1":
                    if self.STATUS == "13411":
                        self.es_manager.update_option_modiport_insert_input(update)
                    elif self.STATUS == "13412":
                        self.es_manager.update_option_modiport_insert_output(update)
                    elif self.STATUS == "13413":
                        self.es_manager.update_option_modiport_insert_exinput(update)
                    elif self.STATUS == "13414":
                        self.es_manager.update_option_modiport_insert_exoutput(update)
                    elif self.STATUS == "13415":
                        self.es_manager.update_option_modiport_insert_internal(update)
                elif self.STATUS[3] == "2":
                    if self.STATUS == "13421":
                        self.es_manager.update_option_modiport_delete_input(update)
                    elif self.STATUS == "13422":
                        self.es_manager.update_option_modiport_delete_output(update)
                    elif self.STATUS == "13423":
                        self.es_manager.update_option_modiport_delete_exinput(update)
                    elif self.STATUS == "13424":
                        self.es_manager.update_option_modiport_delete_exoutput(update)
                    elif self.STATUS == "13425":
                        self.es_manager.update_option_modiport_delete_internal(update)
                else:
                    if self.STATUS == "13431":
                        self.es_manager.update_option_modiport_change_input(update)
                    elif self.STATUS == "13432":
                        self.es_manager.update_option_modiport_change_output(update)

            if self.es_manager is not None:
                if check_operation(self.es_manager.operation_count):
                    # To go back to menu
                    self.operation_TF = False
                    self.es_manager = None
                    self.STATUS = self.STATUS[:-1]
                    if len(self.STATUS) == 0:
                        update.message.reply_text("Please type /start to restart")
                    else:
                        self.print_current_menu(update, context, int(self.STATUS[-1]))

        elif self.STATUS[0] == "2":
            if self.STATUS == "21":
                self.dot_manager.print_entity_dot(update, context)
            elif self.STATUS == "22":
                self.dot_manager.print_coupling_dot_LR(update, context)
            elif self.STATUS == "23":
                self.dot_manager.print_coupling_dot_UD(update, context)

            if self.dot_manager is not None:
                if check_operation(self.dot_manager.operation_count):
                    self.operation_TF = False
                    self.dot_manager = None
                    self.STATUS = self.STATUS[:-1]
                    if len(self.STATUS) == 0:
                        update.message.reply_text("Please type /start to restart")
                    else:
                        self.print_current_menu(update, context, int(self.STATUS[-1]))

        elif self.STATUS[0] == "3":
            if self.STATUS == "31":
                self.synthesis_manager.interactive_pruning(update)
            elif self.STATUS == "32":
                self.synthesis_manager.print_pruned_entity(update)
            elif self.STATUS == "33":
                self.synthesis_manager.delete_pruned_entity(update)
            elif self.STATUS == "34":
                self.synthesis_manager.update_pruned_entity_name(update)

            if self.synthesis_manager is not None:
                if check_operation(self.synthesis_manager.operation_count):
                    self.operation_TF = False
                    self.synthesis_manager = None
                    self.STATUS = self.STATUS[:-1]
                    if len(self.STATUS) == 0:
                        update.message.reply_text("Please type /start to restart")
                    else:
                        self.print_current_menu(update, context, int(self.STATUS[-1]))

        elif self.STATUS[0] == "4":
            if self.STATUS == "41":
                self.em_manager._list_pes(update)
            elif self.STATUS == "42":
                self.em_manager._sim_start(update, context)
            elif self.STATUS == "43":
                self.em_manager._sys_exec(update)
            elif self.STATUS == "44":
                self.em_manager._sys_synthesis(update)

            if self.em_manager is not None:
                if check_operation(self.em_manager.operation_count):
                    self.operation_TF = False
                    self.em_manager = None
                    self.STATUS = self.STATUS[:-1]
                    if len(self.STATUS) == 0:
                        update.message.reply_text("Please type /start to restart")
                    else:
                        self.print_current_menu(update, context, int(self.STATUS[-1]))






