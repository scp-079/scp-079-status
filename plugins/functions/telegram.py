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
from typing import Iterable, Optional, Union

from pyrogram import Client, InlineKeyboardMarkup, ReplyKeyboardMarkup, Message
from pyrogram.errors import ChatAdminRequired, ButtonDataInvalid, ChannelInvalid, ChannelPrivate, FloodWait
from pyrogram.errors import MessageDeleteForbidden, MessageNotModified, PeerIdInvalid

from .etc import delay
from .decorators import retry
from .status import add_extra

# Enable logging
logger = logging.getLogger(__name__)


def delete_messages(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)

        if len(mids) <= 100:
            return delete_messages_100(client, cid, mids)

        mids_list = [mids[i:i + 100] for i in range(0, len(mids), 100)]
        result = bool([delete_messages_100(client, cid, mids) for mids in mids_list])
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def delete_messages_100(client: Client, cid: int, mids: Iterable[int]) -> Optional[bool]:
    # Delete some messages
    result = None

    try:
        mids = list(mids)
        result = client.delete_messages(chat_id=cid, message_ids=mids)
    except FloodWait as e:
        raise e
    except MessageDeleteForbidden:
        return False
    except Exception as e:
        logger.warning(f"Delete messages in {cid} error: {e}", exc_info=True)

    return result


@retry
def edit_message_text(client: Client, cid: int, mid: int, text: str,
                      markup: InlineKeyboardMarkup = None) -> Union[bool, Message, None]:
    # Edit the message's text
    result = None

    try:
        if not text.strip():
            return None

        result = client.edit_message_text(
            chat_id=cid,
            message_id=mid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=markup
        )
    except FloodWait as e:
        add_extra(e)
        raise e
    except ButtonDataInvalid:
        logger.warning(f"Edit message {mid} text in {cid} - invalid markup: {markup}")
    except MessageNotModified:
        return None
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Edit message {mid} in {cid} error: {e}", exc_info=True)

    return result


@retry
def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup] = None) -> Union[bool, Message, None]:
    # Send a message to a chat
    result = None

    try:
        if not text.strip():
            return None

        result = client.send_message(
            chat_id=cid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=mid,
            reply_markup=markup
        )
    except FloodWait as e:
        raise e
    except ButtonDataInvalid:
        logger.warning(f"Send message to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return False
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result


@retry
def send_report_message(secs: int, client: Client, cid: int, text: str, mid: int = None,
                        markup: InlineKeyboardMarkup = None) -> Optional[bool]:
    # Send a message that will be auto deleted to a chat
    result = None

    try:
        if not text.strip():
            return None

        result = client.send_message(
            chat_id=cid,
            text=text,
            parse_mode="html",
            disable_web_page_preview=True,
            reply_to_message_id=mid,
            reply_markup=markup
        )

        if not result:
            return None

        mid = result.message_id
        mids = [mid]
        result = delay(secs, delete_messages, [client, cid, mids])
    except FloodWait as e:
        raise e
    except ButtonDataInvalid:
        logger.warning(f"Send report message to {cid} - invalid markup: {markup}")
    except (ChannelInvalid, ChannelPrivate, ChatAdminRequired, PeerIdInvalid):
        return None
    except Exception as e:
        logger.warning(f"Send report message to {cid} error: {e}", exc_info=True)

    return result
