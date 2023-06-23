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
from os import getcwd, getpid, kill
from signal import SIGABRT
from subprocess import run

from pyrogram import Client

from .. import glovar
from .etc import code, lang
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def restart_program(client: Client, cid: int = 0) -> bool:
    # Restart the program
    result = False

    glovar.locks["restart"].acquire()

    try:
        if cid:
            send_message(client, cid, f"{lang('status')}：{code(lang('restarted'))}\n")
            return True

        service_name = getcwd().split("/")[-1]
        run(f"systemctl --user restart {service_name}", shell=True)
        kill(getpid(), SIGABRT)
    except Exception as e:
        logger.warning(f"Restart program error: {e}", exc_info=True)
    finally:
        glovar.locks["restart"].release()

    return result


def update_program() -> bool:
    # Update the program
    result = False

    glovar.locks["restart"].acquire()

    try:
        service_name = getcwd().split("/")[-1]
        run(f"bash ~/scp-079/scripts/update.sh {service_name}", shell=True)
        run("git pull", shell=True)
        kill(getpid(), SIGABRT)
    except Exception as e:
        logger.warning(f"Update program error: {e}", exc_info=True)
    finally:
        glovar.locks["restart"].release()

    return result
