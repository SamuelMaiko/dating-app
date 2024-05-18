from .GenerateOTP import generate_otp
from userauth.models import EmailOTP

def create_otp_model(user):
    otp=generate_otp()
    EmailOTP.objects.create(user=user, otp=otp)