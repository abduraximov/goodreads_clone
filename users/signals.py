from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail

# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             "Welcome to Goodreads Clone",
#             f"Hi, {instance.username} Welcome to Goodreads clone. Enjoy the books and reviews",
#             "abdurakhimovy@gmail.com",
#             [instance.email]
#         )
