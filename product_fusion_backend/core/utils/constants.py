from typing import Type, TypedDict

from pydantic import BaseModel

from product_fusion_backend.core.schema.common_response_schema import CommonResponseSchema


class RouteOptions(TypedDict):
    response_model_exclude_none: bool
    response_model: Type[BaseModel]


DEFAULT_ROUTE_OPTIONS: RouteOptions = {
    "response_model_exclude_none": True,
    "response_model": CommonResponseSchema,
}

PASSWORD_RESET_MAIL_TEMPLATE = """<html> <body> <p>Hello,</p> <p>You have requested to reset your password. Please
click the link below to reset your password:</p> <a href={}>Reset Password</a> <p>This link will expire in 1
hour.</p> <p>If you did not request this, please ignore this email.</p> </body> </html>"""

INVITE_MEMBER_MAIL_TEMPLATE = """<html> <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2>Invitation to Join Organization</h2> <p>Hello,</p> <p>You've been invited to join an organization on our
platform. To accept this invitation, please click the button below:</p> <p style="text-align: center;"> <a href="{
invite_link}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center;
text-decoration: none; display: inline-block; border-radius: 4px; font-size: 16px;"> Accept Invitation </a> </p>
<p>If the button doesn't work, you can copy and paste this link into your browser:</p> <p>{invite_link}</p> <p>This
invitation will expire in 7 days.</p> <p>If you didn't expect this invitation, you can safely ignore this email.</p>
<p>Best regards,<br>Your Application Team</p> </body> </html>"""

VERIFY_EMAIL_TEMPLATE = """<html> <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2>Welcome to Our Platform!</h2> <p>Hello {},</p> <p>Thank you for signing up. To complete your
registration, please click the button below:</p> <p style="text-align: center;"> <a href="{}"
style="background-color: #4CAF50; color: white; padding: 14px 20px; text-align: center; text-decoration: none;
display: inline-block; border-radius: 4px; font-size: 16px;"> Verify Your Email </a> </p> <p>If the button doesn't
work, you can copy and paste this link into your browser:</p> <p>{}</p> <p>This link will expire in
24 hours.</p> <p>Welcome aboard!</p> <p>Best regards,<br>Your Application Team</p> </body> </html>"""

PASSWORD_UPDATE_MAIL_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2>Password Updated</h2>
    <p>Hello {},</p>
    <p>Your password has been successfully updated.</p>
    <p>If you did not make this change, please contact our support team immediately.</p>
    <p>Best regards,<br>Your Application Team</p>
</body>
</html>
"""

LOGIN_ALERT_MAIL_TEMPLATE = """<html> <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<h2>New Login Detected</h2> <p>Hello {},</p> <p>We detected a new login to your account with the following
details:</p> <ul> <li>Date and Time: {}</li> <li>IP Address: {}</li> <li>Device: {}</li>
</ul> <p>If this was you, you can ignore this email. If you don't recognize this activity, please change your
password immediately and contact our support team.</p> <p>Best regards,<br>Your Application Team</p> </body> </html>"""

VERIFY_EMAIL_WITH_PASS_RESET_TEMPLATE = """
        <html>
        <body>
            <h2>Welcome to Our Platform!</h2>
            <p>Your invite has been accepted. To complete your registration, please follow these steps:</p>
            <ol>
                <li>Click on the verification link below to verify your email:</li>
                <p><a href="{}">Verify Your Email</a></p>
                <li>Use the following temporary password to log in:</li>
                <p><strong>{}</strong></p>
                <li>After logging in, please change your password immediately.</li>
            </ol>
            <p>This verification link and temporary password will expire in 24 hours.</p>
            <p>If you didn't request this invite, please ignore this email.</p>
            <p>Best regards,<br>Your Application Team</p>
        </body>
        </html>
        """

SKIP_URLS = [
    "/api/health",
    "/static/docs/swagger-ui.css",
    "/static/docs/swagger-ui-bundle.js",
    "/api/openapi.json",
    "/api/docs",
    "/api/redoc",
    "/api/auth",
    "/api/auth/login",
    "/api/auth/verify-email",
]
