from django.core.mail import send_mail
from django.conf import settings

def SendWelcomeEmail(user):
    subject="Our Dating App Registration"
    message=f"Hello {user.username},\nWelcome to Our Dating App. An email has been sent for your account activation.\n\nBest Regards,\nDev Team\nOur Dating App"
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    send_mail(subject, message, sender, recipient_list, fail_silently=True)