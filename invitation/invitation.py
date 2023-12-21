from flask_mailman import EmailMessage
from flask import render_template, Response
import app
import os
import importlib
import datetime
import config
from datetime import timezone

import jwt

from flask import g, request


def send_invitation_study(to, token, study_name, role):
    accept_url = f"{config.FAIRHUB_FRONTEND_URL}auth/signup?code={token}&email={to}"
    subject, from_email, to = (f"You have been invited to {study_name} invitation",
                               'aydan.gasimova2@example.com', to)
    html_content = render_template(
        "accept_study_invitation.html",
        token=token,
        accept_url=accept_url,
        study_name=study_name,
        role=role,
        to=to
    )

    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()


def send_access_contributors(to, study, first_name, last_name, role):
    accept_url = f"{config.FAIRHUB_FRONTEND_URL}study/{study.id}/overview"
    subject, from_email, to = (f"You have been invited to {study.title} invitation",
                               'aydan.gasimova2@example.com', to)
    html_content = render_template(
        "accept_study_invitation.html",
        accept_url=accept_url,
        first_name=first_name,
        last_name=last_name,
        study_name=study.title,
        study_id=study.id,
        role=role,
    )

    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()


def send_invitation_general(to, token):
    accept_url = f"{config.FAIRHUB_FRONTEND_URL}auth/signup?code={token}&email={to}"
    subject, from_email, to = (f"You have been invited to signup to FAIRhub",
                               'aydan.gasimova2@example.com', to)
    html_content = render_template(
        "accept_general_invitation.html",
        token=token,
        accept_url=accept_url,
        to=to
    )

    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"
    msg.send()


def send_email_verification(email_address, token):
    verification_url = (
        f"{config.FAIRHUB_FRONTEND_URL}auth/verify-email?email="
        f"{email_address}&token={token}"
    )
    subject, from_email, to = (f"Verify email address",
                               'aydan.gasimova2@example.com', email_address)
    html_content = render_template(
        "email_verification.html",
        token=token,
        verification_url=verification_url,
        email=email_address,
    )
    msg = EmailMessage(subject, html_content, from_email, [email_address])
    msg.content_subtype = "html"
    msg.send()


def signin_notification(user, device_ip):
    user_profile_url = f"{config.FAIRHUB_FRONTEND_URL}studies"
    subject, from_email, to = (f"Login notification",
                               'aydan.gasimova2@example.com', user.email_address)
    html_content = render_template(
        "device_notification.html", user_profile_url=user_profile_url, device_ip=device_ip
    )
    msg = EmailMessage(subject, html_content, from_email, [user.email_address])
    msg.content_subtype = "html"
    msg.send()


def get_config():
    if os.environ.get("FLASK_ENV") == "testing":
        config_module_name = "pytest_config"
    else:
        config_module_name = "config"

    config_module = importlib.import_module(config_module_name)

    if os.environ.get("FLASK_ENV") == "testing":
        # If testing, use the 'TestConfig' class for accessing 'secret'
        config = config_module.TestConfig
    else:
        config = config_module

    return config


# Get list of user ids that have previously authenticated on this device
def get_device_user_list() -> list[str]:
    # FIX THE TYPE OF THE TOKEN["USERS"], IT WAS GETTING ERROR SINCE token returns a dict instead of list
    # Check if cookie exists
    if "token_device" not in request.cookies:
        return []

    # Get value from cookie
    cookie = request.cookies.get("token_device")
    if not cookie:
        return []

    token = {}
    config = get_config()
    try:
        token = jwt.decode(cookie, config.FAIRHUB_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return []

    if "users" not in token:
        return []

    return token["users"]


def add_user_to_device_list(response: Response, user) -> None:
    users = get_device_user_list()
    if user.id not in users:
        users.append(user.id)

    config = get_config()
    expiration = datetime.datetime.now(timezone.utc) + datetime.timedelta(days=365)
    cookie = jwt.encode(
        {
            "users": users,
            "exp": expiration,
        },
        config.FAIRHUB_SECRET,
        algorithm="HS256",
    )

    response.set_cookie(
        "token_device",
        cookie,
        secure=True,
        httponly=True,
        samesite="None",
        expires=expiration,
    )


def check_trusted_device() -> bool:
    users = get_device_user_list()
    for user in users:
        print("User known: " + user)
    return g.user.id in users
