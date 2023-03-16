from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("insuremonkey/", include("insuremonkey.urls")),
]
