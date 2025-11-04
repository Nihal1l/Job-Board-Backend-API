"""
===========================================
utils/email_service.py
===========================================
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_verification_email(user, token):
    """Send email verification link"""
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    subject = 'Verify Your Email - Job Board'
    html_message = f"""
    <html>
        <body>
            <h2>Welcome to Job Board, {user.first_name}!</h2>
            <p>Please click the link below to verify your email address:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account, please ignore this email.</p>
        </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_application_notification(application):
    """Send notification emails when application is submitted"""
    
    # Email to job seeker
    job_seeker_subject = f'Application Submitted - {application.job.title}'
    job_seeker_message = f"""
    <html>
        <body>
            <h2>Application Submitted Successfully</h2>
            <p>Dear {application.applicant.first_name},</p>
            <p>Your application for <strong>{application.job.title}</strong> at <strong>{application.company_name}</strong> has been submitted successfully.</p>
            <p>We'll notify you when the employer reviews your application.</p>
            <p>Application Status: <strong>{application.get_status_display()}</strong></p>
        </body>
    </html>
    """
    
    send_mail(
        job_seeker_subject,
        strip_tags(job_seeker_message),
        settings.DEFAULT_FROM_EMAIL,
        [application.applicant.email],
        html_message=job_seeker_message,
        fail_silently=True,
    )
    
    # Email to employer
    employer_subject = f'New Application - {application.job.title}'
    employer_message = f"""
    <html>
        <body>
            <h2>New Job Application Received</h2>
            <p>Dear {application.job.employer.first_name},</p>
            <p>You have received a new application for <strong>{application.job.title}</strong>.</p>
            <p><strong>Applicant:</strong> {application.applicant.full_name}</p>
            <p><strong>Email:</strong> {application.email}</p>
            <p>Log in to your dashboard to review the application.</p>
        </body>
    </html>
    """
    
    send_mail(
        employer_subject,
        strip_tags(employer_message),
        settings.DEFAULT_FROM_EMAIL,
        [application.job.employer.email],
        html_message=employer_message,
        fail_silently=True,
    )


def send_status_update_notification(application, new_status):
    """Send notification when application status is updated"""
    
    subject = f'Application Status Update - {application.job.title}'
    message = f"""
    <html>
        <body>
            <h2>Application Status Updated</h2>
            <p>Dear {application.applicant.first_name},</p>
            <p>Your application for <strong>{application.job.title}</strong> at <strong>{application.company_name}</strong> has been updated.</p>
            <p><strong>New Status:</strong> {application.get_status_display()}</p>
            {
                '<p>Congratulations! You have been shortlisted for the next round.</p>' 
                if new_status == 'shortlisted' 
                else ''
            }
            {
                '<p>Unfortunately, your application was not selected at this time.</p>' 
                if new_status == 'rejected' 
                else ''
            }
            <p>Log in to your dashboard for more details.</p>
        </body>
    </html>
    """
    
    send_mail(
        subject,
        strip_tags(message),
        settings.DEFAULT_FROM_EMAIL,
        [application.applicant.email],
        html_message=message,
        fail_silently=True,
    )




