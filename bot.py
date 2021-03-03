import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from processed import Processed


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Starting message"
    )


def help(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    update.message.reply_text(
        "Helping message",
        reply_to_message_id=message_id
    )


def get(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    with open("test.json", "rb") as misc:
        file = misc.read()
    # update.message.reply_document('https://i.kym-cdn.com/photos/images/original/001/356/324/914.gif')
    update.message.reply_document(file,
                                  filename='template.json')


def load(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    filename = update.message.document.file_name
    file = context.bot.getFile(update.message.document.file_id)
    parse_file_name = f'{message_id}-{filename}'
    file.download(parse_file_name)

    processed = Processed(filename=parse_file_name)
    processed_message = 'Send Complete'
    if processed.has_error:
        print(processed.err_message)
        processed_message = f'When send some email has raise error: {processed.err_message}'
    update.message.reply_text(
        f'You upload file - {filename} \n\r {processed_message}',
        reply_to_message_id=message_id
    )


def main() -> None:
    # Create the Updater and pass it your bot's token.
    load_dotenv()
    token = os.environ.get('BOT_TOKEN')
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('get', get))
    dispatcher.add_handler(MessageHandler(Filters.document, load))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
