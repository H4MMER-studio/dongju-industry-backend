import smtplib

from src.core import get_settings


def send_email(body):
    try:
        sender = ...

        smtp = smtplib.SMTP(
            host=get_settings().EMAIL_HOST,
            port=get_settings().EMAIL_PORT,
        )
        smtp.sendmail(
            from_addr=sender,
            to_addrs=get_settings().EMAIL_SENDER,
        )

        return

    except Exception as error:
        print(error)
