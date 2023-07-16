import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        params = {"offset": offset, "timeout": timeout}
        response = requests.get(url, params=params)
        response.raise_for_status()

        json_data = response.json()
        return GetUpdatesResponse(**json_data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=data)
        response.raise_for_status()

        json_data = response.json()
        return SendMessageResponse(**json_data)
