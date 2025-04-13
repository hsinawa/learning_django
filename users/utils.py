from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
import ssl


def get_email_html_template(name, company, job_links):
    """
    Generate HTML email content as a string with inline styling
    
    Parameters:
    - name: Applicant's name
    - company: Company name
    - job_links: List of dictionaries with job titles and URLs
    
    Returns:
    - HTML email content as a string
    """
    
    # Create job links HTML
    job_links_html = ""
    for job in job_links:
        job_links_html += f'all good\n'
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Application</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="margin-bottom: 20px;">
        <p>Dear Hiring Manager at <span style="font-weight: bold; color: #0066cc;">{company}</span>,</p>
    </div>
    
    <div>
        <p>My name is {name}, and I am reaching out to express my interest in exploring software development opportunities at {company}.</p>
        
        <p>I recently came across your organization and was impressed by your innovative work in the tech industry. With my background in software development and passion for creating efficient, user-friendly solutions, I believe I could be a valuable addition to your team.</p>
        
        <p>I'm particularly interested in the following positions:</p>
        
        <div style="margin: 20px 0;">
            {job_links_html}
        </div>
        
        <p>I have attached my resume for your review, which details my experience, technical skills, and professional accomplishments. My expertise includes full-stack development, problem-solving, and working effectively in collaborative environments.</p>
        
        <p>I would welcome the opportunity to discuss how my skills and experience align with your team's needs. Thank you for considering my application.</p>
    </div>
    
    <div style="margin-top: 30px;">
        <p>Best regards,</p>
        <p>{name}</p>
    </div>
</body>
</html>'''
    

def send_verification_email(user, request, token):
    try:
        base_url = request.build_absolute_uri('/')[:-1]
        params = urlencode({'uid': user.id, 'token': token})
        verification_url = f"{base_url}/api/users/verify-email?{params}"

        subject = "Verify your email for our project"
        body = f"""
        Hi {user.name},

        Thank you for registering! Please verify your email address by clicking the link below:

        {verification_url}

        If you didn’t sign up for this account, you can ignore this email.

        Regards,
        Your Project Team
        """
        print(f"Sending verification email to {verification_url}")
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.send(fail_silently=False)
        return verification_url
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        