from django.urls import path
from .views import recognize_image

urlpatterns = [
    path('recognize/', recognize_image, name='recognize_image'),
]
