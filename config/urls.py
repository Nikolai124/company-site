from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
    path("consent/", views.consent, name="consent"),
]
