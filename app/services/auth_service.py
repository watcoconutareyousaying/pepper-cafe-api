import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MAILTRAP_USER")
pwd = os.getenv("MAILTRAP_PASS")
print(f"MAILTRAP_USER={user}, MAILTRAP_PASS={pwd}")


def send_password_mail(email: str, password: str):
    msg = EmailMessage()
    msg["subject"] = "Your Cafe system login password"
    msg["From"] = os.getenv("EMAIL_SENDER") or "Cafe Admin <admin@cafe.com>"
    msg["To"] = email
    msg.set_content(
        f"""\
            Welcome to Pepper Cafe!

            Here are your login credentials:
            Email: {email}
            Password: {password}

            Please keep this information secure.

            Thank you for joining us!
        """
    )

    try:
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as smtp:
            smtp.starttls()
            smtp.login(user, pwd)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")