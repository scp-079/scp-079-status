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
import pickle
from configparser import RawConfigParser
from os.path import exists
from random import randint
from threading import Lock
from typing import Dict, List, Union

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
RESTART_PATH = "data/config/restart.txt"
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

# [pyrogram]
api_id: int = 0
api_hash: str = "[DATA EXPUNGED]"

# [proxy]
enabled: Union[bool, str] = "False"
hostname: str = "127.0.0.1"
port: int = 1080

# [auth]
creator_id: int = 0

# [basic]
bot_token: str = ""
ipv6: Union[bool, str] = "False"
prefix: List[str] = []
prefix_str: str = "/!"
restart: int = 19

# [channels]
critical_channel_id: int = 0

# [custom]
format_date: str = ""
format_time: str = ""
interval: int = 0
manual_link: str = "https://manuals.scp-079.org/bots/status/"

# [language]
lang: str = ""

try:
    not exists(CONFIG_PATH) and raise_error(f"{CONFIG_PATH} does not exists")
    config = RawConfigParser()
    config.read(CONFIG_PATH)

    # [pyrogram]
    api_id = int(config.get("pyrogram", "api_id", fallback=api_id))
    api_hash = config.get("pyrogram", "api_hash", fallback=api_hash)

    # [proxy]
    enabled = config.get("proxy", "enabled", fallback=enabled)
    enabled = eval(enabled)
    hostname = config.get("proxy", "hostname", fallback=hostname)
    port = int(config.get("proxy", "port", fallback=port))

    # [auth]
    creator_id = int(config.get("auth", "creator_id", fallback=str(creator_id)))

    # [basic]
    bot_token = config.get("basic", "bot_token", fallback=bot_token)
    ipv6 = config.get("basic", "ipv6", fallback=ipv6)
    ipv6 = eval(ipv6)
    prefix = [p for p in list(config.get("basic", "prefix", fallback=prefix_str)) if p]
    restart = int(config.get("basic", "restart", fallback=str(restart)))

    # [channels]
    critical_channel_id = int(config.get("channels", "critical_channel_id", fallback=str(critical_channel_id)))

    # [custom]
    format_date = config.get("custom", "format_date", fallback=format_date)
    format_time = config.get("custom", "format_time", fallback=format_time)
    interval = int(config.get("custom", "interval", fallback=str(interval)))
    manual_link = config.get("custom", "manual_link", fallback=manual_link)

    # [language]
    lang = config.get("language", "lang", fallback=lang)

    # [flag]
    broken = False
except Exception as e:
    print(f"[ERROR] Read data from {CONFIG_PATH} error, please check the log file")
    logger.warning(f"Read data from {CONFIG_PATH} error: {e}", exc_info=True)

# Check
check_all(
    {
        "pyrogram": {
            "api_id": api_id,
            "api_hash": api_hash
        },
        "proxy": {
            "enabled": enabled,
            "hostname": hostname,
            "port": port
        },
        "auth": {
            "creator_id": creator_id
        },
        "basic": {
            "bot_token": bot_token,
            "ipv6": ipv6,
            "prefix": prefix,
            "restart": restart
        },
        "channels": {
            "critical_channel_id": critical_channel_id
        },
        "custom": {
            "format_date": format_date,
            "format_time": format_time,
            "interval": interval,
            "manual_link": manual_link
        },
        "language": {
            "lang": lang
        }
    },
    broken
)

# Postprocess - [proxy]
if enabled:
    proxy = {
        "hostname": hostname,
        "port": port,
        "scheme": "socks5"
    }
else:
    proxy = None

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
    "edit": Lock(),
    "file": Lock(),
    "restart": Lock()
}

sender: str = "STATUS"

updating: bool = False

version: str = "0.1.8"

# Load data from TXT file

if exists(REPORT_PATH):
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report_text = f.read()
else:
    report_text = ""

if exists(RESTART_PATH):
    with open(RESTART_PATH, "r", encoding="utf-8") as f:
        restart_text = f.read()
        restart_text = restart_text.strip()
else:
    restart_text = str(randint(4, 14))
    with open(RESTART_PATH, "w", encoding="utf-8") as f:
        f.write(restart_text)

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
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
