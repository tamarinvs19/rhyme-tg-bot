from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import config as cfg
import rhyme


def help_command(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
            Commands:
            /help  Show help
            /start Say hello
            <text> Find rhyme
        """,
    )


def start_bot(update, context):
    user = update.effective_user
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hi {user.full_name}!',
    )


def rhyme_command(update, context):
    answer = rhyme.find_rhyme(update.message.text)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
    )


def main_bot():
    updater = Updater(cfg.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_bot))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, rhyme_command)
    )

    updater.start_webhook(listen="0.0.0.0",
                          port=cfg.PORT,
                          url_path=cfg.TOKEN)
    updater.bot.setWebhook(f'https://{cfg.APPNAME}.herokuapp.com/' + cfg.TOKEN)
    updater.idle()


if __name__ == '__main__':
    main_bot()
