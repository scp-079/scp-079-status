# SCP-079-STATUS - Check Linux server status
# Copyright (C) 2019-2023 SCP-079 <https://scp-079.org>
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

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from .. import glovar
from .etc import code, lang, get_text, thread
from .telegram import send_message, send_report_message

# Enable logging
logger = logging.getLogger(__name__)


def command_error(client: Client, message: Message, action: str, error: str,
                  detail: str = "", report: bool = True, private: bool = False) -> bool:
    # Command error
    result = False

    try:
        # Basic data
        cid = message.chat.id
        uid = message.from_user.id
        mid = message.id

        # Generate the text
        if private:
            text = ""
        else:
            text = f"{lang('user_id')}{lang('colon')}{code(uid)}\n"

        text += (f"{lang('action')}{lang('colon')}{code(action)}\n"
                 f"{lang('status')}{lang('colon')}{code(lang('status_failed'))}\n"
                 f"{lang('reason')}{lang('colon')}{code(error)}\n")

        if detail:
            text += f"{lang('detail')}{lang('colon')}{code(detail)}\n"

        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=lang("read_manual"),
                        url=glovar.manual_link
                    )
                ]
            ]
        )

        # Send the message
        if report:
            send_report_message(10, client, cid, text, None, markup)
        else:
            thread(send_message, (client, cid, text, mid, markup))

        result = True
    except Exception as e:
        logger.warning(f"Command error: {e}", exc_info=True)

    return result


def get_command_context(message: Message) -> (str, str):
    # Get the type "a" and the context "b" in "/command a b"
    command_type = ""
    command_context = ""

    try:
        text = get_text(message)
        command_list = text.split()

        if len(list(filter(None, command_list))) <= 1:
            return "", ""

        i = 1
        command_type = command_list[i]

        while command_type == "" and i < len(command_list):
            i += 1
            command_type = command_list[i]

        command_context = text[1 + len(command_list[0]) + i + len(command_type):].strip()
    except Exception as e:
        logger.warning(f"Get command context error: {e}", exc_info=True)

    return command_type, command_context


def get_command_type(message: Message) -> str:
    # Get the command type "a" in "/command a"
    result = ""

    try:
        text = get_text(message)
        command_list = list(filter(None, text.split()))
        result = text[len(command_list[0]):].strip()
    except Exception as e:
        logger.warning(f"Get command type error: {e}", exc_info=True)

    return result
