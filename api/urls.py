from django.urls import path

from .views import log_message, recognize_image

urlpatterns = [
    path("recognize/", recognize_image, name="recognize_image"),
    path("logs/", log_message, name="log_message"),
]
