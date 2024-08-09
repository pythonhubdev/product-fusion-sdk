from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP

from product_fusion_backend.settings import settings


class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str) -> bool:
        message = MIMEMultipart()
        message["From"] = settings.smtp_username
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        try:
            smtp = SMTP(hostname=settings.smtp_server, port=settings.smtp_port, use_tls=True)
            await smtp.connect()
            await smtp.login(settings.smtp_username, settings.smtp_password)
            await smtp.send_message(message)
            await smtp.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False


email_service = EmailService()
