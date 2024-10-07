from django.urls import path
from MEM_MED import views


urlpatterns = [

    path("medicine/", views.daily_medicine_detail.as_view(), name="show_course"),
    path("calendar/", views.calendar.as_view(), name="calendar"),
    path("calendar/<int:year>/<int:month>/", views.calendar.as_view(), name="calendar"),
    path('day/<int:year>/<int:month>/<int:day>/', views.day_view, name='day_view'),  # You'll need to create this view
]