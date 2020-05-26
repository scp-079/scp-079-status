# SCP-079-STATUS - Check Linux server status
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-STATUS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pyrogram import Client, Filters, Message

from .. import glovar
from ..functions.command import command_error
from ..functions.etc import code, lang, thread
from ..functions.file import save
from ..functions.filters import creator_user, from_user
from ..functions.group import delete_message
from ..functions.status import get_status
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.private & Filters.command(["start"], glovar.prefix)
                   & from_user & creator_user)
def start(client: Client, message: Message) -> bool:
    # Start the bot
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Generate the text
        text = (f"{lang('commands')}{lang('colon')}\n\n"
                f"/send {code('-')} {lang('command_send')}\n"
                f"/new {code('-')} {lang('command_new')}\n")

        # Send the report message
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"Start error: {e}", exc_info=True)

    return result


@Client.on_message(Filters.incoming & Filters.private & Filters.command(["new"], glovar.prefix)
                   & from_user & creator_user)
def new(client: Client, message: Message) -> bool:
    # Send a new status message
    result = False

    glovar.locks["edit"].acquire()

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Check current message id
        if not glovar.message_id:
            return command_error(client, message, lang("action_send"), lang("command_usage"), lang("error_none"))

        # Generate the text
        text = get_status()

        # Send the status message
        delete_message(client, glovar.critical_channel_id, glovar.message_id)
        result = send_message(client, glovar.critical_channel_id, text, mid)

        if not result:
            return command_error(client, message, lang("action_send"), lang("error_send"))

        # Update the message id
        glovar.message_id = result.message_id
        save("message_id")

        # Send the report message
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_new'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('status_succeeded'))}\n")
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"New error: {e}", exc_info=True)
    finally:
        glovar.locks["edit"].release()

    return result


@Client.on_message(Filters.incoming & Filters.private & Filters.command(["send"], glovar.prefix)
                   & from_user & creator_user)
def send(client: Client, message: Message) -> bool:
    # Send a status message
    result = False

    glovar.locks["edit"].acquire()

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Check current message id
        if glovar.message_id:
            return command_error(client, message, lang("action_send"), lang("command_usage"), lang("error_already"))

        # Generate the text
        text = get_status()

        # Send the status message
        result = send_message(client, glovar.critical_channel_id, text, mid)

        if not result:
            return command_error(client, message, lang("action_send"), lang("error_send"))

        # Update the message id
        glovar.message_id = result.message_id
        save("message_id")

        # Send the report message
        text = (f"{lang('action')}{lang('colon')}{code(lang('action_send'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('status_succeeded'))}\n")
        thread(send_message, (client, cid, text, mid))

        result = True
    except Exception as e:
        logger.warning(f"Send error: {e}", exc_info=True)
    finally:
        glovar.locks["edit"].release()

    return result
