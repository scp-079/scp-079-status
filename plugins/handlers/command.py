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
from subprocess import run, PIPE

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import glovar
from ..functions.command import command_error, get_command_type
from ..functions.etc import code, general_link, get_int, get_readable_time, lang, thread
from ..functions.file import save
from ..functions.filters import creator_user, from_user
from ..functions.group import delete_message
from ..functions.program import restart_program, update_program
from ..functions.status import get_status
from ..functions.telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(filters.incoming & filters.private & filters.command(["start", "help"], glovar.prefix)
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


@Client.on_message(filters.incoming & filters.private & filters.command(["new"], glovar.prefix)
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
            return command_error(client, message, lang("action_send"), lang("command_usage"),
                                 lang("error_none"), False)

        # Generate the text
        text = get_status()

        # Send the status message
        delete_message(client, glovar.critical_channel_id, glovar.message_id)
        result = send_message(client, glovar.critical_channel_id, text, mid)

        if not result:
            return command_error(client, message, lang("action_send"), lang("error_send"), report=False)

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


@Client.on_message(filters.incoming & filters.command(["restart"], glovar.prefix)
                   & from_user & creator_user)
def restart(client: Client, message: Message) -> bool:
    # Restart the program
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Generate the text
        text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('action')}{lang('colon')}{code(lang('program_restart'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('command_received'))}\n")

        # Send the report message
        send_message(client, cid, text, mid)

        # Restart the program
        result = restart_program()
    except Exception as e:
        logger.warning(f"Restart error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.private & filters.command(["send"], glovar.prefix)
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
            return command_error(client, message, lang("action_send"), lang("command_usage"),
                                 lang("error_already"), False)

        # Generate the text
        text = get_status()

        # Send the status message
        result = send_message(client, glovar.critical_channel_id, text, mid)

        if not result:
            return command_error(client, message, lang("action_send"), lang("error_send"), report=False)

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


@Client.on_message(filters.incoming & filters.command(["update"], glovar.prefix)
                   & from_user & creator_user)
def update(client: Client, message: Message) -> bool:
    # Update the program
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Check update status
        if glovar.updating:
            text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                    f"{lang('status')}{lang('colon')}{code(lang('program_updating'))}\n")
            return thread(send_message, (client, cid, text, mid))

        # Generate the text
        text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('action')}{lang('colon')}{code(lang('program_update'))}\n"
                f"{lang('status')}{lang('colon')}{code(lang('command_received'))}\n")

        # Send the report message
        send_message(client, cid, text, mid)

        # Update the program
        glovar.updating = True
        result = update_program()
    except Exception as e:
        logger.warning(f"Update error: {e}", exc_info=True)

    return result


@Client.on_message(filters.incoming & filters.command(["version"], glovar.prefix)
                   & from_user & creator_user)
def version(client: Client, message: Message) -> bool:
    # Check the program's version
    result = False

    try:
        # Basic data
        cid = message.chat.id
        mid = message.message_id

        # Get command type
        command_type = get_command_type(message)

        # Check the command type
        if command_type and command_type.upper() != glovar.sender:
            return False

        # Check update status
        if glovar.updating:
            text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                    f"{lang('status')}{lang('colon')}{code(lang('program_updating'))}\n")
            return thread(send_message, (client, cid, text, mid))

        # Version info
        git_change = bool(run("git diff-index HEAD --", stdout=PIPE, shell=True).stdout.decode().strip())
        git_date = run("git log -1 --format='%at'", stdout=PIPE, shell=True).stdout.decode()
        git_date = get_readable_time(get_int(git_date), "%Y/%m/%d %H:%M:%S")
        git_hash = run("git rev-parse --short HEAD", stdout=PIPE, shell=True).stdout.decode()
        get_hash_link = f"https://github.com/scp-079/scp-079-{glovar.sender.lower()}/commit/{git_hash}"
        command_date = get_readable_time(message.date, "%Y/%m/%d %H:%M:%S")

        # Generate the text
        text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('version')}{lang('colon')}{code(glovar.version)}\n"
                f"{lang('git_change')}{lang('colon')}{code(git_change)}\n"
                f"{lang('git_hash')}{lang('colon')}{general_link(git_hash, get_hash_link)}\n"
                f"{lang('git_date')}{lang('colon')}{code(git_date)}\n"
                f"{lang('command_date')}{lang('colon')}{code(command_date)}\n")

        # Send the report message
        result = send_message(client, cid, text, mid)
    except Exception as e:
        logger.warning(f"Version error: {e}", exc_info=True)

    return result
