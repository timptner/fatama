from urllib.parse import urljoin

import requests

from django.conf import settings
from markdown import markdown

DOMAIN = "https://api.postmarkapp.com"

HTTP_CODES = {
    200: "Success",
    401: "Unauthorized",
    404: "Entity doesn't exist",
    413: "Payload Too Large",
    415: "Unsupported Media Type",
    422: "Unprocessable Entity",
    429: "Rate Limit Exceeded",
    500: "Internal Server Error",
    503: "Service Unavailable",
}


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
        if status != 200:
            answer = HTTP_CODES[status]
            if status == 422:
                data = response.json()
                code = data["ErrorCode"]
                message = data["Message"]
                answer = f"{answer} (ErrorCode: {code}, Message: {message})"
            raise Exception(answer)

        data = response.json()

        error = data["ErrorCode"]
        if error != 0:
            raise Exception(f"Unsupported error code: {error}")

        return status == 200 and error == 0
