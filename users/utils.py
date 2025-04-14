from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
import ssl
from django.utils.html import strip_tags


    

def send_verification_email(user, request, token):
    try:
        base_url = request.build_absolute_uri('/')[:-1]
        params = urlencode({'uid': user.id, 'token': token})
        verification_url = f"{base_url}/api/users/verify-email?{params}"

        subject = "🔐 Verify Your Email Address - Project Name"
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 40px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">Hi {user.name},</h2>
                <p style="font-size: 16px; color: #555;">
                    Thank you for registering with <strong>Our Project</strong>! <br/>
                    Please confirm your email address by clicking the button below:
                </p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background-color: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; font-size: 16px; border-radius: 5px;">
                        Verify Email
                    </a>
                </div>
                <p style="font-size: 14px; color: #888;">
                    If the button above doesn’t work, paste this link into your browser:<br/>
                    <a href="{verification_url}" style="color: #4CAF50;">{verification_url}</a>
                </p>
                <hr style="margin: 30px 0;" />
                <p style="font-size: 13px; color: #999;">
                    If you did not create an account, you can safely ignore this email.
                </p>
                <p style="font-size: 14px; color: #777;">Warm regards,<br/><strong>Your Project Team</strong></p>
            </div>
        </body>
        </html>
        """

        text_content = strip_tags(html_content)

        email = EmailMessage(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        print(f" Verification email sent to {user.email}")
        return verification_url

    except Exception as e:
        print(f" Failed to send verification email: {e}")
        