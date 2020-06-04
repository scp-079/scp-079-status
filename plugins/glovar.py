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
from os import mkdir
from os.path import exists
from shutil import rmtree
from threading import Lock
from typing import Dict, List

from yaml import safe_load

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    filename="log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Read data from config.ini

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
    config = RawConfigParser()
    config.read("config.ini")

    # [auth]
    creator_id = int(config["auth"].get("creator_id", str(creator_id)))

    # [basic]
    bot_token = config["basic"].get("bot_token", bot_token)
    prefix = list(config["basic"].get("prefix", prefix_str))

    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", str(critical_channel_id)))

    # [custom]
    format_date = config["custom"].get("format_date", format_date)
    format_time = config["custom"].get("format_time", format_time)
    interval = int(config["custom"].get("interval", str(interval)))

    # [language]
    lang = config["language"].get("lang", lang)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (False
        # [auth]
        or creator_id == 0

        # [basic]
        or bot_token in {"", "[DATA EXPUNGED]"}
        or prefix == []

        # [channels]
        or critical_channel_id == 0

        # [custom]
        or format_date in {"", "[DATA EXPUNGED]"}
        or format_time in {"", "[DATA EXPUNGED]"}
        or interval == 0

        # [language]
        or lang in {"", "[DATA EXPUNGED]"}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Language Dictionary
lang_dict: dict = {}

try:
    with open(f"languages/{lang}.yml", "r", encoding="utf-8") as f:
        lang_dict = safe_load(f)
except Exception as e:
    logger.critical(f"Reading language YAML file failed: {e}", exc_info=True)
    raise SystemExit("Reading language YAML file failed")

# Init

all_commands: List[str] = [
    "start",
    "new",
    "send"
]

extra: float = 0

locks: Dict[str, Lock] = {
    "edit": Lock()
}

sender: str = "STATUS"

version: str = "0.0.7"

# Load data from TXT file

with open("report.txt", "r", encoding="utf-8") as f:
    report = f.read()

# Load data from pickle

# Init dir
try:
    rmtree("tmp")
except Exception as e:
    logger.info(f"Remove tmp error: {e}")

for path in ["data", "tmp"]:
    if not exists(path):
        mkdir(path)

# Init data

message_id: int = 0

# Load data
file_list: List[str] = ["message_id"]

for file in file_list:
    try:
        try:
            if exists(f"data/{file}") or exists(f"data/.{file}"):
                with open(f"data/{file}", "rb") as f:
                    locals()[f"{file}"] = pickle.load(f)
            else:
                with open(f"data/{file}", "wb") as f:
                    pickle.dump(eval(f"{file}"), f)
        except Exception as e:
            logger.error(f"Load data {file} error: {e}", exc_info=True)

            with open(f"data/.{file}", "rb") as f:
                locals()[f"{file}"] = pickle.load(f)
    except Exception as e:
        logger.critical(f"Load data {file} backup error: {e}", exc_info=True)
        raise SystemExit("[DATA CORRUPTION]")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
