from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Post, Newsletter


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, **kwargs):
    email_subscribers = Newsletter.objects.values_list('email', flat=True)
    subject = 'Новый пост опубликован'
    message = f'Пост "{instance.header}" опубликован на сайте.'
    send_mail(subject, message, 'your_email', email_subscribers, fail_silently=False)

