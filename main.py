#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client

from plugins import glovar
from plugins.functions.timers import interval_min_10, interval_sec_n, log_rotation
from plugins.start import init, renew

# Enable logging
logger = logging.getLogger(__name__)

# Init
init()

# Renew session
renew()

# Config session
app = Client(
    session_name="bot",
    bot_token=glovar.bot_token
)
app.start()

# Start update
sleep(glovar.interval)
interval_sec_n(app)

# Timer
scheduler = BackgroundScheduler(job_defaults={"misfire_grace_time": 60})
scheduler.add_job(interval_min_10, "interval", minutes=10)
scheduler.add_job(log_rotation, "cron", hour=23, minute=59)
scheduler.start()

# Hold
app.idle()

# Stop
app.stop()
