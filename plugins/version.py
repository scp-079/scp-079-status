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

from os import listdir, mkdir, remove
from os.path import exists, isfile, join
from shutil import move, rmtree


def delete_file(path: str) -> bool:
    # Delete a file
    result = False

    try:
        if not(path and exists(path)):
            return False

        result = remove(path) or True
    except Exception as e:
        print(f"Delete file error: {e}")

    return result


def move_file(src: str, dst: str) -> bool:
    # Move a file
    result = False

    try:
        if not src or not exists(src) or not dst:
            return False

        result = bool(move(src, dst))
    except Exception as e:
        print(f"Move file error: {e}")

    return result


def remove_dir(path: str) -> bool:
    # Remove a directory
    result = False

    try:
        if not path or not exists(path):
            return False

        result = rmtree(path) or True
    except Exception as e:
        print(f"Remove dir error: {e}")

    return result


def files(path):
    # List files, not directories
    for file in listdir(path):
        if isfile(join(path, file)):
            yield file


def version_0() -> bool:
    # Version 0
    result = False

    try:
        exists("data/tmp") and rmtree("data/tmp")

        for path in ["data", "data/config", "data/pickle", "data/pickle/backup",
                     "data/log", "data/session", "data/tmp"]:
            not exists(path) and mkdir(path)

        result = True
    except Exception as e:
        print(f"Version 0 error: {e}")

    return result


def version_0_0_9() -> bool:
    # Version 0.0.9
    result = False

    try:
        if exists("data/pickle/current"):
            return False

        move_file("config.ini", "data/config/config.ini")
        move_file("report.txt", "data/config/report.txt")
        move_file("log", "data/log/log")

        for file in files("data"):
            if file.startswith("."):
                file = file[1:]
                move_file(f"data/.{file}", f"data/pickle/backup/{file}")
            else:
                move_file(f"data/{file}", f"data/pickle/{file}")

        move_file("bot.session", "data/session/bot.session")
        remove_dir("tmp")

        result = True
    except Exception as e:
        print(f"Version 0.0.9 error: {e}")

    return result


def version_control() -> bool:
    # Version control
    result = False

    try:
        version_0()

        version_0_0_9()

        result = True
    except Exception as e:
        print(f"Version control error: {e}")

    return result
