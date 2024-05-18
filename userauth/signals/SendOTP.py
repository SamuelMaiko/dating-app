from django.dispatch import Signal, receiver
from userauth.models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings

send_otp_signal=Signal()

@receiver(send_otp_signal, sender=None)
def send_otp_signal_handler(sender, **kwargs):
    user=kwargs["user"]
    otp=EmailOTP.objects.filter(user=user).first().otp
    subject=f"{user.username}, here's your OTP"
    message=f"Hi {user.username},\n\nEnter this code to verify your email.\n\n{otp}\n\nBest Regards,\nDev Team\nOur Dating App"
    sender=settings.EMAIL_HOST_USER
    recipient_list=[user.email]
    
    send_mail(subject, message, sender, recipient_list, fail_silently=True)
    