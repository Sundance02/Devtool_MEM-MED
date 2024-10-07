from django.urls import path
from MEM_MED import views


urlpatterns = [

    path("medicine/", views.daily_medicine_detail.as_view(), name="show_course"),
]