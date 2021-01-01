# SCP-079-STATUS - Check Linux server status
# Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>
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
from os.path import exists

# Enable logging
logger = logging.getLogger(__name__)


def check_all(values: dict, broken: bool) -> bool:
    # Check all values in config.ini
    error = ""

    sections = list(values)
    sections.sort()

    for section in sections:
        data = values[section]
        error += eval(f"check_{section}")(data, broken)

    if not error:
        return True

    raise_error(error)


def check_auth(values: dict, broken: bool) -> str:
    # Check all values in auth section
    result = ""

    for key in values:
        if key == "creator_id" and values[key] <= 0:
            result += f"[ERROR] [auth] {key} - please fill a positive integer\n"

        if not broken or not result:
            continue

        raise_error(result)

    return result


def check_basic(values: dict, broken: bool) -> str:
    # Check all values in basic section
    result = ""

    for key in values:
        if key == "bot_token" and values[key] in {"", "[DATA EXPUNGED]"}:
            result += f"[ERROR] [basic] {key} - please fill a valid token\n"
        elif key == "prefix" and (isinstance(values[key], str) or not values[key]):
            result += f"[ERROR] [basic] {key} - please fill a valid command prefix list\n"

        if not broken or not result:
            continue

        raise_error(result)

    return result


def check_channels(values: dict, broken: bool) -> str:
    # Check all values in channels section
    result = ""

    for key in values:
        if values[key] >= 0:
            result += f"[ERROR] [channels] {key} - should be a negative integer\n"
        elif key.endswith("channel_id") and not str(values[key]).startswith("-100"):
            result += f"[ERROR] [channels] {key} - please use a channel instead\n"
        elif not str(values[key]).startswith("-100"):
            result += f"[ERROR] [channels] {key} - please use a supergroup instead\n"

        if not broken or not result:
            continue

        raise_error(result)

    return result


def check_custom(values: dict, broken: bool) -> str:
    # Check all values in custom section
    result = ""

    for key in values:
        if values[key] in {"", "[DATA EXPUNGED]"}:
            result += f"[ERROR] [custom] {key} - please fill something except [DATA EXPUNGED]\n"
        elif key.endswith("link") and (values[key].startswith("@") or " " in values[key] or "." not in values[key]):
            result += f"[ERROR] [custom] {key} - please input a valid url\n"
        elif key == "interval" and not values[key]:
            result += f"[ERROR] [custom] {key} - should be a positive value\n"

        if not broken or not result:
            continue

        raise_error(result)

    return result


def check_language(values: dict, broken: bool) -> str:
    # Check all values in language section
    result = ""

    for key in values:
        if key == "lang" and values[key] in {"", "[DATA EXPUNGED]"}:
            result += f"[ERROR] [language] {key} - please fill something except [DATA EXPUNGED]\n"
        elif key == "lang" and not exists(f"languages/{values[key]}.yml"):
            result += f"[ERROR] [language] {key} - language {values[key]} does not exist\n"

        if not broken or not result:
            continue

        raise_error(result)

    return result


def raise_error(error: str):
    error = "-" * 24 + f"\nBot refused to start because:\n" + "-" * 24 + f"\n{error}" + "-" * 24
    logger.critical("\n" + error)
    raise SystemExit(error)
