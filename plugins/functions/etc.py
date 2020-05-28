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
from datetime import datetime
from html import escape
from json import dumps
from random import choice, uniform
from string import ascii_letters, digits
from threading import Thread, Timer
from time import gmtime, localtime, sleep, strftime, time
from typing import Any, Callable, Optional, Union

from pyrogram import Message
from pyrogram.errors import FloodWait

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def bold(text: Any) -> str:
    # Get a bold text
    result = ""

    try:
        result = str(text).strip()

        if not result:
            return ""

        result = f"<b>{escape(result)}</b>"
    except Exception as e:
        logger.warning(f"Bold error: {e}", exc_info=True)

    return result


def button_data(action: str, action_type: str = None, data: Union[int, str] = None) -> Optional[bytes]:
    # Get a button's bytes data
    result = None

    try:
        button = {
            "a": action,
            "t": action_type,
            "d": data
        }
        result = dumps(button).replace(" ", "").encode("utf-8")
    except Exception as e:
        logger.warning(f"Button data error: {e}", exc_info=True)

    return result


def code(text: Any) -> str:
    # Get a code text
    result = ""

    try:
        result = str(text).strip()

        if not result:
            return ""

        result = f"<code>{escape(result)}</code>"
    except Exception as e:
        logger.warning(f"Code error: {e}", exc_info=True)

    return result


def code_block(text: Any) -> str:
    # Get a code block text
    result = ""

    try:
        result = str(text).rstrip()

        if not result:
            return ""

        result = f"<pre>{escape(result)}</pre>"
    except Exception as e:
        logger.warning(f"Code block error: {e}", exc_info=True)

    return result


def delay(secs: int, target: Callable, args: list = None) -> bool:
    # Call a function with delay
    result = False

    try:
        t = Timer(secs, target, args)
        t.daemon = True
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Delay error: {e}", exc_info=True)

    return result


def general_link(text: Union[int, str], link: str) -> str:
    # Get a general link
    result = ""

    try:
        text = str(text).strip()
        link = link.strip()

        if not (text and link):
            return ""

        result = f'<a href="{link}">{escape(text)}</a>'
    except Exception as e:
        logger.warning(f"General link error: {e}", exc_info=True)

    return result


def get_int(text: str) -> Optional[int]:
    # Get a int from a string
    result = None

    try:
        result = int(text)
    except Exception as e:
        logger.info(f"Get int error: {e}", exc_info=True)

    return result


def get_now() -> int:
    # Get time for now
    result = 0

    try:
        result = int(time())
    except Exception as e:
        logger.warning(f"Get now error: {e}", exc_info=True)

    return result


def get_readable_time(secs: int = 0, the_format: str = "%Y%m%d%H%M%S") -> str:
    # Get a readable time string
    result = ""

    try:
        if secs:
            result = datetime.utcfromtimestamp(secs).strftime(the_format)
        else:
            result = strftime(the_format, localtime())
    except Exception as e:
        logger.warning(f"Get readable time error: {e}", exc_info=True)

    return result


def get_text(message: Message) -> str:
    # Get message's text
    result = ""

    try:
        if not message:
            return ""

        the_text = message.text or message.caption

        if not the_text:
            return ""

        result += the_text
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return result


def get_time_str(secs: int, the_format: str = "%H:%M:%S") -> str:
    # Get a time string
    result = ""

    try:
        result = strftime(the_format, gmtime(secs))
        days = int(secs // (60 * 60 * 24))

        if not days:
            return result

        result = f"{days} {lang('days')} {result}"
    except Exception as e:
        logger.warning(f"Get time str error: {e}", exc_info=True)

    return result


def lang(text: str) -> str:
    # Get the text
    result = ""

    try:
        result = glovar.lang_dict.get(text, text)
    except Exception as e:
        logger.warning(f"Lang error: {e}", exc_info=True)

    return result


def random_str(i: int) -> str:
    # Get a random string
    result = ""

    try:
        result = "".join(choice(ascii_letters + digits) for _ in range(i))
    except Exception as e:
        logger.warning(f"Random str error: {e}", exc_info=True)

    return result


def thread(target: Callable, args: tuple, kwargs: dict = None, daemon: bool = True) -> bool:
    # Call a function using thread
    result = False

    try:
        t = Thread(target=target, args=args, kwargs=kwargs, daemon=daemon)
        t.daemon = daemon
        result = t.start() or True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return result


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    result = False

    try:
        result = sleep(e.x + uniform(0.5, 1.0)) or True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return result
