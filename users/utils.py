from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
import ssl
from django.utils.html import strip_tags


    

def send_verification_email(user, request, token):
    try:
        base_url = 'https://learningdjango-804594827915.asia-south1.run.app/api'
        params = urlencode({'uid': user.id, 'token': token})
        verification_url = f"{base_url}/api/users/verify-email?{params}"

        subject = "Verify Your Email Address - BCG Assessment by Awanish"
        html_content = f"""
        <html>
       <body style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f7f9fc; padding: 40px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                <h2 style="color: #1a1a1a; font-size: 24px; font-weight: 600; margin: 0 0 20px;">Hi {user.name},</h2>
                <p style="font-size: 16px; color: #4a4a4a; line-height: 1.6; margin: 0 0 24px;">
                    Thank you for registering with <strong style="color: #1a1a1a;">Our Project</strong>! <br>
                    Please confirm your email address by clicking the button below:
                </p>
                <div style="text-align: center; margin: 32px 0;">
                    <a href="{verification_url}" 
                    style="display: inline-block; background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 14px 32px; text-decoration: none; font-size: 16px; font-weight: 500; border-radius: 8px; transition: transform 0.2s ease, box-shadow 0.2s ease;"
                    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                        Verify Email
                    </a>
                </div>
                <p style="font-size: 14px; color: #6b7280; line-height: 1.5; margin: 0 0 24px;">
                    If the button doesn’t work, paste this link into your browser:<br>
                    <a href="{verification_url}" style="color: #4CAF50; text-decoration: none; font-weight: 500;">{verification_url}</a>
                </p>
                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 32px 0;" />
                <p style="font-size: 13px; color: #9ca3af; line-height: 1.5; margin: 0 0 16px;">
                    If you did not create an account, you can safely ignore this email.
                </p>
                <p style="font-size: 14px; color: #6b7280; line-height: 1.5; margin: 0;">
                    Warm regards,<br><strong style="color: #1a1a1a;">Your Project Team</strong>
                </p>
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
        email.send(fail_silently=False)

        print(f" Verification email sent to {user.email}")
        return verification_url

    except Exception as e:
        print(f" Failed to send verification email: {e}")
        