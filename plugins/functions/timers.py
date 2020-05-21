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
from time import sleep

from pyrogram import Client

from .. import glovar
from .etc import delay
from .file import save
from .group import delete_message
from .status import get_status
from .telegram import edit_message_text, send_message

# Enable logging
logger = logging.getLogger(__name__)


def interval_min_10() -> bool:
    # Execute every 10 minutes
    result = False

    try:
        if glovar.extra <= 0:
            return False

        if glovar.interval < 3:
            return False

        glovar.extra -= 0.1
        logger.warning(f"Decreased extra waiting to {glovar.extra}")

        result = True
    except Exception as e:
        logger.warning(f"Interval min 10 error: {e}", exc_info=True)

    return result


def interval_sec_n(client: Client) -> bool:
    # Execute every N seconds
    result = False

    if glovar.extra > 0:
        sleep(glovar.extra)

    delay(glovar.interval, interval_sec_n, [client])

    if not glovar.message_id:
        return False

    if not glovar.locks["edit"].acquire(blocking=False):
        return False

    try:
        text = get_status()

        result = edit_message_text(
            client=client,
            cid=glovar.critical_channel_id,
            mid=glovar.message_id,
            text=text
        )

        if result is not False:
            return bool(result)

        result = send_message(
            client=client,
            cid=glovar.critical_channel_id,
            text=text
        )

        if not result:
            return False

        delete_message(client, glovar.critical_channel_id, glovar.message_id)
        glovar.message_id = result.message_id
        save("message_id")

        result = True
    except Exception as e:
        logger.warning(f"Interval sec n error: {e}", exc_info=True)
    finally:
        glovar.locks["edit"].release()

    return result
