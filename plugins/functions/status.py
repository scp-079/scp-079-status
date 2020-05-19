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
from distro import linux_distribution
from platform import uname
from socket import gethostname

from psutil import boot_time, cpu_count, cpu_freq

from .. import glovar
from .etc import get_now, get_readable_time, get_time_str

# Enable logging
logger = logging.getLogger(__name__)


def get_cpu_count_logical(text: str) -> str:
    # Get logical CPU count
    result = text

    try:
        codename = "$cpu_count_logical$"

        if codename not in text:
            return result

        status = str(cpu_count(logical=True))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu count logical error: {e}", exc_info=True)

    return result


def get_cpu_count_physical(text: str) -> str:
    # Get physical CPU count
    result = text

    try:
        codename = "$cpu_count_physical$"

        if codename not in text:
            return result

        status = str(cpu_count(logical=False))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu count physical error: {e}", exc_info=True)

    return result


def get_cpu_freq_current(text: str) -> str:
    # Get CPU current frequency
    result = text

    try:
        codename = "$freq_current$"

        if codename not in text:
            return result

        status = f"{cpu_freq().current:.2f}Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq current error: {e}", exc_info=True)

    return result


def get_cpu_freq_max(text: str) -> str:
    # Get CPU max frequency
    result = text

    try:
        codename = "$freq_max$"

        if codename not in text:
            return result

        status = f"{cpu_freq().max:.2f}Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq max error: {e}", exc_info=True)

    return result


def get_cpu_freq_min(text: str) -> str:
    # Get CPU max frequency
    result = text

    try:
        codename = "$freq_max$"

        if codename not in text:
            return result

        status = f"{cpu_freq().min:.2f}Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq min error: {e}", exc_info=True)

    return result


def get_dist(text: str) -> str:
    # Get dist
    result = text

    try:
        codename = "$dist$"

        if codename not in text:
            return result

        status = " ".join(d for d in linux_distribution()[:-1])

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get dist error: {e}", exc_info=True)

    return result


def get_hostname(text: str) -> str:
    # Get the hostname
    result = text

    try:
        codename = "$hostname$"

        if codename not in text:
            return result

        status = gethostname()

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get hostname error: {e}", exc_info=True)

    return result


def get_interval(text: str) -> str:
    # Get update interval
    result = text

    try:
        codename = "$interval$"

        if codename not in text:
            return result

        status = str(glovar.interval)

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get interval error: {e}", exc_info=True)

    return result


def get_kernel(text: str) -> str:
    # Get current kernel
    result = text

    try:
        codename = "$kernel$"

        if codename not in text:
            return result

        status = uname().release

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get kernel error: {e}", exc_info=True)

    return result


def get_last(text: str) -> str:
    # Get last seen time
    result = text

    try:
        codename = "$last$"

        if codename not in text:
            return result

        status = get_readable_time(the_format=glovar.format_date)

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get last error: {e}", exc_info=True)

    return result


def get_status() -> str:
    # Get system status
    result = glovar.report

    try:
        # Basic
        result = get_interval(result)
        result = get_last(result)

        # System
        result = get_dist(result)
        result = get_kernel(result)
        result = get_hostname(result)
        result = get_up_time(result)

        # CPU
        result = get_cpu_count_physical(result)
        result = get_cpu_count_logical(result)
        result = get_cpu_freq_max(result)
        result = get_cpu_freq_min(result)
        result = get_cpu_freq_current(result)
    except Exception as e:
        logger.warning(f"Get status error: {e}", exc_info=True)

    return result


def get_up_time(text: str) -> str:
    # Get system up time
    result = text

    try:
        codename = "$up_time$"

        if codename not in text:
            return result

        status = get_time_str(
            secs=get_now() - boot_time(),
            the_format=glovar.format_time
        )

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get up time error: {e}", exc_info=True)

    return result
