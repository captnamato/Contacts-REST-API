"""
Сервіс для відправки email
"""
import os
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "noreply@contacts-api.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Contacts API"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)

fastmail = FastMail(conf)


async def send_verification_email(email: str, verification_token: str, base_url: str):
    """Відправка email для верифікації"""
    verification_url = f"{base_url}/api/v1/auth/verify-email?token={verification_token}"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Підтвердження реєстрації</title>
    </head>
    <body>
        <h2>Ласкаво просимо до Contacts API!</h2>
        <p>Для завершення реєстрації, будь ласка, підтвердіть вашу електронну адресу:</p>
        <a href="{verification_url}" style="
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
        ">Підтвердити email</a>
        <p>Або скопіюйте це посилання у браузер:</p>
        <p>{verification_url}</p>
        <p>Якщо ви не реєструвались на нашому сайті, просто проігноруйте цей лист.</p>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Підтвердження реєстрації в Contacts API",
        recipients=[email],
        body=html_content,
        subtype=MessageType.html
    )

    await fastmail.send_message(message)
