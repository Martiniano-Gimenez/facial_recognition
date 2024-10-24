import os

from django.contrib import admin
from django.db import models


def upload_to(instance, filename):
    base_path = "static/img/"
    legajo = instance.legajo
    extension = os.path.splitext(filename)[1]
    counter = 1
    while os.path.exists(
        os.path.join(f"media/{base_path}", f"{legajo}_{counter}{extension}")
    ):
        counter += 1

    return f"{base_path}{legajo}_{counter}{extension}"


class ReferenceImage(models.Model):
    name = models.CharField(max_length=100)
    legajo = models.CharField(max_length=6)
    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Register the model in the admin site
admin.site.register(ReferenceImage)

from django.db.models.signals import post_delete
from django.dispatch import receiver
from PIL import Image


@receiver(post_delete, sender=ReferenceImage)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
