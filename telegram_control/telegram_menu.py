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
        self.es_manager = telegram_entityManager()

    def print_current_menu(self, update, current_num):
        if current_num == 1:
            if len(self.STATUS) == 1:
                update.message.reply_text("1. Create new Entity")
                update.message.reply_text("2. Read Entity")
                update.message.reply_text("3. Update Entity")
                update.message.reply_text("4. Delete Entity")
                update.message.reply_text("0. Exit")
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.setting_step(update)
                    self.operation_TF = True
        elif current_num == 2:
            if len(self.STATUS) == 1:
                # model management
                update.message.reply_text(self.STATUS)
            elif len(self.STATUS) == 2:
                if self.STATUS[0] == "1":
                    self.setting_step(update)
                    self.operation_TF = True

        elif current_num == "0":
            if self.STATUS == "":
                update.message.reply_text("over")
        else:
            update.message.reply_text(self.STATUS)

    def setting_step(self, update):
        if self.STATUS[0] == "1":
            if self.STATUS == "11":
                self.es_manager.create_option(update)
            elif self.STATUS == "12":
                self.es_manager.read_option(update)
            print(self.es_manager.operation_count)
            if check_operation(self.es_manager.operation_count):
                self.operation_TF = False
                self.STATUS = self.STATUS[:-1]
                self.print_current_menu(update, int(self.STATUS[0]))
