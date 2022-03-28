import logging
import os

from dialogflow_search_intent import get_answer_from_dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from setup_logger import setup_logger


logger = logging.getLogger(__file__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!"
    )


def process_message(
    update: Update,
    context: CallbackContext
):

    dialogflow_intent_response = get_answer_from_dialogflow(
        project_id=context.bot_data['project_id'],
        session_id=update.effective_chat.id,
        texts=update.message.text
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=dialogflow_intent_response.query_result.fulfillment_text
    )


def main():

    setup_logger()

    logger.info('Starting Game of Verbs TG bot')

    try:
        updater = Updater(token=os.environ['TG_TOKEN'])
        dispatcher = updater.dispatcher
        dispatcher.bot_data['project_id'] = os.environ['DIALOGFLOW_PROJECT_ID']

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        typical_question_handler = MessageHandler(
            Filters.text & (~Filters.command),
            process_message
        )

        dispatcher.add_handler(typical_question_handler)

        updater.start_polling()
    except ConnectionError:
        logger.exception('ConnectionError messages bot')
    except Exception as e:
        logger.exception('Unexpected exception has occured')
        raise e


if __name__ == '__main__':
    main()
