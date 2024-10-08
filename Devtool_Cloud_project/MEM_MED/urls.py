from django.urls import path
from MEM_MED import views

urlpatterns = [
    path("medicine/", views.daily_medicine_detail.as_view(), name="show_course"),
    path("calendar/", views.calendar.as_view(), name="calendar"),
    path("calendar/<int:year>/<int:month>/", views.calendar.as_view(), name="calendar"),
    path('day/<int:year>/<int:month>/<int:day>/', views.day_view, name='day_view'),  # You'll need to create this view
    path("medicine/add/", views.MedicineAddView.as_view(), name="add-medicine"),
    path("medicine/edit/<int:pk>/", views.MedicineEditView.as_view(), name="edit-medicine"),
    path("medicine/delete/<int:pk>/", views.MedicineDeleteView.as_view(), name="delete-medicine"),
    path("daily-medicine/add/", views.DailyMedicineAddView.as_view(), name="add-daily-medicine"),
]
