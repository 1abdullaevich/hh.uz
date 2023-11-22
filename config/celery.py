import os
# from celery import Celery, shared_task
from django.conf import settings
from django.core.mail import send_mail

#
# # Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from blogs.models import Post


#
# app = Celery("pixelcraft")
#
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#
# # @app.task()
def sent_otp(otp, email, subject):
    send_mail(
        subject,
        f"Your otp: {otp}",
        "aninimusanogus66@gmail.com",
        [email],
        fail_silently=False,
    )
    return True
#
#
# # @shared_task
# def unlike_post(post_id):
#     post = Post.objects.get(id=post_id)
#     post.likes_count = post.likes.all().count()
#     post.save()
