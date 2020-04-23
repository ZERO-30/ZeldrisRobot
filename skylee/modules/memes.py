import random, re
import requests as r

from time import sleep
from typing import Optional, List
from requests import get
from random import randint

from telegram import Message, Update, Bot, User, ParseMode, MessageEntity
from telegram.ext import Filters, CommandHandler, MessageHandler, run_async
from telegram import TelegramError, Chat, Message
from telegram.error import BadRequest
from telegram.utils.helpers import mention_html, escape_markdown

from skylee.modules.helper_funcs.extraction import extract_user
from skylee.modules.helper_funcs.filters import CustomFilters
from skylee.modules.helper_funcs.fun_strings import RUN_STRINGS, SLAP_TEMPLATES, PUNCH_TEMPLATES, HUG_TEMPLATES, ITEMS, THROW, HIT, PUNCH, HUG, ABUSE_STRINGS
from skylee import dispatcher, OWNER_ID, WALL_API
from skylee.modules.disable import DisableAbleCommandHandler


@run_async
def runs(update, context):
    update.effective_message.reply_text(random.choice(RUN_STRINGS))


@run_async
def slap(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        slapped_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(context.bot.first_name, context.bot.id)
        user2 = curr_user

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)

@run_async
def punch(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        punched_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if punched_user.username:
            user2 = "@" + escape_markdown(punched_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(punched_user.first_name,
                                                   punched_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(context.bot.first_name, context.bot.id)
        user2 = curr_user

    temp = random.choice(PUNCH_TEMPLATES)
    item = random.choice(ITEMS)
    punch = random.choice(PUNCH)

    repl = temp.format(user1=user1, user2=user2, item=item, punches=punch)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)



@run_async
def hug(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id:
        hugged_user = context.bot.get_chat(user_id)
        user1 = curr_user
        if hugged_user.username:
            user2 = "@" + escape_markdown(hugged_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(hugged_user.first_name,
                                                   hugged_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "Awwh! [{}](tg://user?id={})".format(context.bot.first_name, context.bot.id)
        user2 = curr_user

    temp = random.choice(HUG_TEMPLATES)
    hug = random.choice(HUG)

    repl = temp.format(user1=user1, user2=user2, hug=hug)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@run_async
def abuse(update, context):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(ABUSE_STRINGS))

@run_async
def shrug(update, context):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text("¯\_(ツ)_/¯")

@run_async
def decide(update, context):
        r = randint(1, 100)
        if r <= 65:
            update.message.reply_text("Yes.")
        elif r <= 90:
            update.message.reply_text("NoU.")
        else:
            update.message.reply_text("Maybe.")

@run_async
def snipe(update, context):
    args = context.args
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text("Please give me a chat to echo to!")     
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            context.bot.sendMessage(int(chat_id), str(to_send))        
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))             
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")


# Bug reporting module for x00td ports grp...
@run_async
def ports_bug(update, context):
    message = update.effective_message
    user = update.effective_user
    bug = message.text[len('/bug '):]

    if not bug:
        message.reply_text("Submitting empty bug report won't do anything!")
        return

    if bug:
        context.bot.sendMessage(-1001495581911, "<b>NEW BUG REPORT!</b>\n\n<b>Submitted by</b>: {}.\n\nDescription: <code>{}</code>.".format(mention_html(user.id, user.first_name), bug), parse_mode=ParseMode.HTML)
        message.reply_text("Successfully submitted bug report!")


__help__ = """
Some dank memes for ya all!

 - /shrug : get shrug 🤷
 - /decide : Randomly answers yes/no/maybe
 - /abuse : Abuses the retard!
 - /runs: Reply a random string from an array of replies.
 - /slap: Slap a user, or get slapped if not a reply.
 - /warm: Hug a user warmly, or get hugged if not a reply.
 - /punch: Punch a user, or get punched if not a reply.
"""

__mod_name__ = "Memes"

SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)
SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True, filters=CustomFilters.sudo_filter)
ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
PORT_BUG_HANDLER = CommandHandler("bug", ports_bug, filters=Filters.chat(-1001297379754))
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True)
PUNCH_HANDLER = DisableAbleCommandHandler("punch", punch, pass_args=True)
HUG_HANDLER = DisableAbleCommandHandler("warm", hug, pass_args=True)

dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(PORT_BUG_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
