from flask_mail import Message
from flask import render_template
import app
import os
import importlib
from urllib.parse import urlparse, parse_qs


def send_invitation_study(to, token, study_name, role):
    accept_url = f"http://localhost:3000/auth/signup?code={token}&email={to}"
    msg = Message(
        subject=f"You have been invited to {study_name} invitation",
        sender="aydan.gasimova2@example.com",
        recipients=[to],
    )
    msg.html = render_template(
        "accept_study_invitation.html",
        token=token,
        accept_url=accept_url,
        study_name=study_name,
        role=role
    )
    app.mail.send(msg)


def send_access_contributors(to, study, first_name, last_name, role):
    accept_url = f"http://localhost:3000/study/{study.id}/overview"
    msg = Message(
        subject=f"You have been invited to {study.title} invitation",
        sender="aydan.gasimova2@example.com",
        recipients=[to],
    )
    msg.html = render_template(
        "invite_contributors.html",
        accept_url=accept_url,
        first_name=first_name,
        last_name=last_name,
        study_name=study.title,
        study_id=study.id,
        role=role
    )
    app.mail.send(msg)


def send_invitation_general(to, token):
    accept_url = f"http://localhost:3000/auth/signup?code={token}&email={to}"
    msg = Message(
        subject=f"You have been invited to signup to FAIRhub",
        sender="aydan.gasimova@example.com",
        recipients=[to],
    )
    msg.html = render_template(
        "accept_general_invitation.html", token=token, accept_url=accept_url
    )
    app.mail.send(msg)


def send_email_verification(email_address, token):
    verification_url =\
        (f"http://localhost:3000/auth/verify-email?email="
         f"{email_address}&token={token}")
    msg = Message(
        subject=f"Verify email address",
        sender="aydan.gasimova@example.com",
        recipients=[email_address],
    )
    msg.html = render_template(
        "email_verification.html",
        token=token,
        verification_url=verification_url,
        email=email_address
    )
    app.mail.send(msg)


def signin_notification(user):
    user_profile = f"http://localhost:3000/studies"
    msg = Message(
        subject=f"Login notification",
        sender="aydan.gasimova@example.com",
        recipients=[user.email_address],
    )
    msg.html = render_template(
        "accept_general_invitation.html", user_profile=user_profile
    )
    app.mail.send(msg)


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
# def get_device_user_list() -> list[str]:
#     # FIX THE TYPE OF THE TOKEN["USERS"], IT WAS GETTING ERROR SINCE token returns a dict instead of list
#     # Check if cookie exists
#     if "token_device" not in request.cookies:
#         return []
#
#     # Get value from cookie
#     cookie = request.cookies.get("token")
#     if not cookie:
#         return []
#
#     token = []
#     config = get_config()
#     try:
#         token = jwt.decode(cookie, config.FAIRHUB_SECRET, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         return []
#     return token["users"]
#
#
# def add_user_to_device_list(response: Response, user) -> None:
#     users = get_device_user_list()
#     if user.id not in users:
#         users.append(user.id)
#
#     config = get_config()
#     expiration = datetime.datetime.now(timezone.utc) + datetime.timedelta(days=365)
#     cookie = jwt.encode(
#         {
#             "users": users,
#             "exp": expiration,
#         },
#         config.FAIRHUB_SECRET,
#         algorithm="HS256",
#     )
#
#     response.set_cookie(
#         "token_device", cookie, secure=True, httponly=True, samesite="None", expires=expiration
#     )


# def check_trusted_device() -> bool:
#     if not g.user:
#         return False
#     users = get_device_user_list()
#     return g.user.id in users

