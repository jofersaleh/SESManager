import logging
#from remote_control.remote_manager import *
#import telegram
#import telegram.ext
#from sample.ses_manager import *
from system_manager.system_manager import *
from telegram_control.telegram_menu import *

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pathlib import Path

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


Remote_control = Remote_telegram()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('You can build your own simulation environment')
    update.message.reply_text("type /help for information")
    if Remote_control.STATUS == "":
        update.message.reply_text("System Management System\n1. Entity Management\n2. Model Management"
                                  "\n3. Model Synthesis\n4. Execution Management\n0. Exit")
    else:
        Remote_control.STATUS = ""
        update.message.reply_text("System Management System\n1. Entity Management\n2. Model Management"
                                  "\n3. Model Synthesis\n4. Execution Management\n0. Exit")



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('new : create new system')
    print(Remote_control.STATUS)



def echo(update, context):
    """Echo the user message."""
    if Remote_control.operation_TF:
        Remote_control.setting_step(update)
    else:
        if update.message.text[0] == "1":
            Remote_control.STATUS += "1"
            Remote_control.print_current_menu(update, 1)
        elif update.message.text[0] == "2":
            Remote_control.STATUS += "2"
            Remote_control.print_current_menu(update, 2)
        elif update.message.text[0] == "3":
            Remote_control.STATUS += "3"
            Remote_control.print_current_menu(update, 3)
        elif update.message.text[0] == "4":
            Remote_control.STATUS += "4"
            Remote_control.print_current_menu(update, 4)
        elif update.message.text[0] == "5":
            Remote_control.STATUS += "5"
            Remote_control.print_current_menu(update, 5)
        elif update.message.text[0] == "0":
            Remote_control.STATUS = Remote_control.STATUS[:-1]
            if Remote_control.STATUS == "":
                start(update, context)
            else:
                Remote_control.print_current_menu(update, int(Remote_control.STATUS[-1]))
        else:
            update.message.reply_text("please type right number")

def load_ses():
    #load ses manager
    if not os.path.exists('./sample/ses_db'):
        os.mkdir('./sample/ses_db')

    if not os.path.exists('./sample/pes_db'):
        os.mkdir('./sample/pes_db')

    if not os.path.exists('./sample/model_db'):
        os.mkdir('./sample/model_db')

    esm = EntityManager("./sample/ses_db")

    entity = esm.create_entity_structure()
    entity.set_name("Agent")

    msa = ModelStructuralAttribute()
    msa.insert_input_port("env")
    msa.insert_input_port("agent")

    msa.insert_output_port("env")
    msa.insert_output_port("agent")

    msa.insert_entity("sensors", 1, True)
    msa.insert_entity("processor", 2, False)
    msa.insert_entity("actuators", 1, False)

    msa.insert_coupling(("", "env"), ("sensors", "env"))
    msa.insert_coupling(("", "agent"), ("sensors", "agent"))

    msa.insert_coupling(("sensors", "event"), ("process", "event"))
    msa.insert_coupling(("processor", "control"), ("actuators", "control"))

    msa.insert_coupling(("actuators", "out"), ("", "out"))

    entity.set_core_attribute(msa)

    esm.export_system_entity_structure(entity, "./sample/ses_db")
    sm = SystemManager("./sample/ses_db", "./sample/model_db", './sample/pes_db')



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    access_lst = open("./telegram_control/auth", 'r')
    access_key = ""
    for data in access_lst:
        access_key = data
    updater = Updater(access_key, use_context=True)






    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()