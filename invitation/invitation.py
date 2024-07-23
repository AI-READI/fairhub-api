from flask import render_template

import config
from azure.communication.email import EmailClient


def azure_email_connection(html_content, subject, to: str):
    connection_string = config.FAIRHUB_SMTP_CONNECTION_STRING
    email_client = EmailClient.from_connection_string(connection_string)
    message = {
        "content": {
            "subject": subject,
            "html": html_content
        },
        "recipients": {
            "to": [
                {
                    "address": to,
                    "displayName": "Customer Name"
                }
            ]
        },
        "senderAddress": config.FAIRHUB_SMTP_SENDER_EMAIL_ADDRESS
    }

    email_client.begin_send(message)
    # poller = email_client.begin_send(message)
    # result = poller.result()


def forgot_password(to, first_name, last_name, token):
    forgot_password_ = f"{config.FAIRHUB_FRONTEND_URL}auth/reset-password?token={token}"

    html_content = render_template(
        "forgot_password.html",
        forgot_password_=forgot_password_,
        email=to,
        first_name=first_name,
        last_name=last_name
    )
    subject, from_email, to = (
                f" Password Change",
                "aydan.gasimova2@example.com",
                to,
    )
    azure_email_connection(html_content, subject, to)


def reset_password(to, first_name, last_name):
    reset_password_ = f"{config.FAIRHUB_FRONTEND_URL}/user/profile"

    html_content = render_template(
        "reset_password.html",
        reset_password_=reset_password_,
        email=to,
        first_name=first_name,
        last_name=last_name
    )
    subject, from_email, to = (
                f" Password Change",
                "aydan.gasimova2@example.com",
                to,
    )
    azure_email_connection(html_content, subject, to)

