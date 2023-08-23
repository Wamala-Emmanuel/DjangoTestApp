import smtplib

def sending_email():
    sender = "otimtonyjeff@gmail.com"
    receiver = "otimtonyjeff@gmail.com"

    message = f"""\
    Subject: Hi Mailtrap this is just a test
    To: {receiver}
    From: {sender}

    This is a test e-mail message."""

    with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        server.login("0f106cd8e4eaa7", "81e8adb348be02")
        server.sendmail(sender, receiver, message)
