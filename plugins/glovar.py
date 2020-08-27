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
import pickle
from configparser import RawConfigParser
from os.path import exists
from threading import Lock
from typing import Dict, List

from yaml import safe_load

from .checker import check_all, raise_error
from .version import version_control

# Path variables
CONFIG_PATH = "data/config/config.ini"
CUSTOM_LANG_PATH = "data/config/custom.yml"
LOG_PATH = "data/log"
PICKLE_BACKUP_PATH = "data/pickle/backup"
PICKLE_PATH = "data/pickle"
REPORT_PATH = "data/config/report.txt"
SESSION_DIR_PATH = "data/session"
SESSION_PATH = "data/session/bot.session"

# Version control
version_control()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename=f"{LOG_PATH}/log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [flag]
broken: bool = True

# [auth]
creator_id: int = 0

# [basic]
bot_token: str = ""
prefix: List[str] = []
prefix_str: str = "/!"

# [channels]
critical_channel_id: int = 0

# [custom]
format_date: str = ""
format_time: str = ""
interval: int = 0

# [language]
lang: str = ""

try:
    not exists(CONFIG_PATH) and raise_error(f"{CONFIG_PATH} does not exists")
    config = RawConfigParser()
    config.read(CONFIG_PATH)

    # [auth]
    creator_id = int(config["auth"].get("creator_id", str(creator_id)))

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = [p for p in list(config["basic"].get("prefix", prefix_str)) if p]

    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", str(critical_channel_id)))

    # [custom]
    format_date = config["custom"].get("format_date", format_date)
    format_time = config["custom"].get("format_time", format_time)
    interval = int(config["custom"].get("interval", str(interval)))

    # [language]
    lang = config["language"].get("lang", lang)

    # [flag]
    broken = False
except Exception as e:
    print(f"[ERROR] Read data from {CONFIG_PATH} error, please check the log file")
    logger.warning(f"Read data from {CONFIG_PATH} error: {e}", exc_info=True)

# Check
check_all(
    {
        "auth": {
            "creator_id": creator_id
        },
        "basic": {
            "bot_token": bot_token,
            "prefix": prefix
        },
        "channels": {
            "critical_channel_id": critical_channel_id
        },
        "custom": {
            "format_date": format_date,
            "format_time": format_time,
            "interval": interval
        },
        "language": {
            "lang": lang
        }
    },
    broken
)

# Language Dictionary
lang_dict: dict = {}
LANG_PATH = CUSTOM_LANG_PATH if exists(CUSTOM_LANG_PATH) else f"languages/{lang}.yml"

try:
    with open(LANG_PATH, "r", encoding="utf-8") as f:
        lang_dict = safe_load(f)
except Exception as e:
    logger.critical(f"Reading language YAML file failed: {e}", exc_info=True)
    raise SystemExit("Reading language YAML file failed")

# Init

all_commands: List[str] = [
    "help",
    "new",
    "restart",
    "start",
    "send",
    "update"
]

extra: float = 0

locks: Dict[str, Lock] = {
    "edit": Lock()
}

sender: str = "STATUS"

updating: bool = False

version: str = "0.1.1"

# Load data from TXT file

if exists(REPORT_PATH):
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report_text = f.read()
else:
    report_text = ""

# Load data from pickle

# Init data

current: str = ""

message_id: int = 0

token: str = ""

# Load data
file_list: List[str] = ["message_id",
                        "current", "token"]

for file in file_list:
    try:
        try:
            if exists(f"{PICKLE_PATH}/{file}") or exists(f"{PICKLE_BACKUP_PATH}/{file}"):
                with open(f"{PICKLE_PATH}/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"{PICKLE_PATH}/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"{PICKLE_BACKUP_PATH}/{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
