from system_manager.system_manager import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_control.telegram_es_manager import *


def check_operation(count):
    if count == 0:
        return True
    else:
        return False


class Remote_telegram():
    def __init__(self):
        self.STATUS = ""
        self.operation_TF = False
        self.es_manager = None

    def print_current_menu(self, update, current_num):
        print(self.STATUS)
        if current_num == 1:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. Create new Entity\n2. Read Entity\n"
                                          "3. Update Entity\n4. Delete Entity\n0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.es_manager = telegram_entityManager()
                    self.setting_step(update)
                    self.operation_TF = True
            elif len(self.STATUS) == 3:
                if self.STATUS[0] == "1":
                    if self.STATUS[1] == "3":
                        self.es_manager = telegram_entityManager()
                        self.setting_step(update)
                        self.operation_TF = True

        elif current_num == 2:
            if len(self.STATUS) == 1:
                # model management
                update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.es_manager = telegram_entityManager()
                    self.setting_step(update)
                    self.operation_TF = True
            elif len(self.STATUS) == 3:
                if self.STATUS[0] == "1":
                    if self.STATUS[1] == "3":
                        self.es_manager = telegram_entityManager()
                        self.setting_step(update)
                        self.operation_TF = True

        elif current_num == 3:
            if len(self.STATUS) == 1:
                #Model Synthesis
                update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    update.message.reply_text("What did you want to modify entity\n1. Add Entity\n2. Delete Entity"
                                              "\n3. Modify Entity\n4. Modify Port\n0. Exit")
            elif len(self.STATUS) == 3:
                if self.STATUS[0] == "1":
                    if self.STATUS[1] == "3":
                        # modify entity
                        update.message.reply_text(self.STATUS)

        elif current_num == 4:
            if len(self.STATUS) == 1:
                #Execution Management
                update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    #Delete Entity
                    update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 3:
                if self.STATUS[0] == "1":
                    if self.STATUS[1] == "3":
                        #4 modify port
                        update.message.reply_text(self.STATUS)

        '''
        elif current_num == "0":
            if self.STATUS == "":
                update.message.reply_text("over")
        else:
            self.print_current_menu(update,self.STATUS[-1])
        '''
    def setting_step(self, update):
        if self.STATUS[0] == "1":
            if self.STATUS == "11":
                self.es_manager.create_option(update)
            elif self.STATUS == "12":
                self.es_manager.read_option(update)
            elif self.STATUS == "131":
                self.es_manager.update_option_addenti(update)
            elif self.STATUS == "132":
                self.es_manager.update_option_deletenti(update)
            if self.es_manager is not None:
                if check_operation(self.es_manager.operation_count):
                    self.operation_TF = False
                    self.es_manager = None
                    self.STATUS = self.STATUS[:-1]
                    self.print_current_menu(update, int(self.STATUS[-1]))
