import os
from typing import List
from requests import Response, post
from libs.strings import gettext


class MailGunException(Exception):
    def __init__(message: str):
        super().__init__(message)


class MailGun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_EMAIL = os.environ.get("FROM_EMAIL")
    FROM_TITLE = "Stores REST API - Flask"

    @classmethod
    def send_email(
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(gettext("mailgun_failed_load_api_key"))
        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(gettext("mailgun_failed_load_domain"))

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailGunException(gettext("mailgun_error_send_email"))

        return response
