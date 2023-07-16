from dataclasses import dataclass
from typing import List

import marshmallow
import marshmallow_dataclass


@dataclass
class Chat:
    id: int
    type: str


@dataclass
class MessageFrom:
    id: int
    first_name: str
    last_name: str


@dataclass
class Message:
    message_id: int
    text: str
    chat: Chat
    from_: MessageFrom


@dataclass
class Update:
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Update]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE
