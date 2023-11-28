from flask_mail import Message
from flask import render_template
import app


def send_invitation_study(to, token, study_name, role):
    accept_url = f"http://localhost:3000/auth/signup?code=${token}&email=${to}"
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
    accept_url = f"http://localhost:3000/auth/signup?code=${token}&email=${to}"
    msg = Message(
        subject=f"You have been invited to signup to FAIRhub",
        sender="aydan.gasimova@example.com",
        recipients=to,
    )
    msg.html = render_template(
        "accept_general_invitation.html", token=token, accept_url=accept_url
    )
    app.mail.send(msg)
