import logging

from urllib.parse import urljoin

import requests

from django.conf import settings
from markdown import markdown

logger = logging.getLogger(__name__)

DOMAIN = "https://api.postmarkapp.com"


class Mail:
    endpoint = "/email"
    headers = {
        "X-Postmark-Server-Token": settings.POSTMARK_API_TOKEN,
    }

    def __init__(
        self,
        tag: str,
        subject: str,
        text: str,
        recipient: str,
        sender: str = settings.DEFAULT_FROM_EMAIL,
        stream: str = "outbound",
    ) -> None:
        self.tag = tag
        self.subject = subject
        self.text = text
        self.html = markdown(text)
        self.recipient = recipient
        self.sender = sender
        self.stream = stream

    def send(self) -> bool:
        url = urljoin(DOMAIN, self.endpoint)
        payload = {
            "From": self.sender,
            "To": self.recipient,
            "Subject": self.subject,
            "TextBody": self.text,
            "HtmlBody": self.html,
            "Tag": self.tag,
            "MessageStream": self.stream,
        }
        response = requests.post(url, json=payload, headers=self.headers)

        status = response.status_code
        if status == 401:
            logger.error("Missing authorization header")

        if status == 422:
            logger.error("Missing sender signature for email sender")

        if status != 200:
            logger.error("Unsupported status code: %d", status)

        data = response.json()

        error = data["ErrorCode"]
        if error != 0:
            logger.warning("Unsupported error code: %d", error)

        return status == 200 and error == 0
