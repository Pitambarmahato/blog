from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def send_verification(sender, instance, created, **kwargs):
    if created:
        # print(instance)
        msg = EmailMultiAlternatives(
            #subject
            "SignUp Successful", 
            #message
            "You have been signed up successfully", 
            #from
            "pitambar@gmail.com", 
            #to
            ("test@gmail.com",))
        msg.send()

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    instance.profile_user.save()