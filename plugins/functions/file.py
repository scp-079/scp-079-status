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
from pickle import dump
from shutil import copyfile

from .. import glovar
from .decorators import threaded

# Enable logging
logger = logging.getLogger(__name__)


@threaded(daemon=False)
def save(file: str) -> bool:
    # Save a global variable to a file
    result = False

    try:
        if not glovar:
            return False

        with open(f"data/.{file}", "wb") as f:
            dump(eval(f"glovar.{file}"), f)

        result = copyfile(f"data/.{file}", f"data/{file}") or True
    except Exception as e:
        logger.warning(f"Save error: {e}", exc_info=True)

    return result
