from django.urls import path
from MEM_MED import views

urlpatterns = [
    path("", views.calendar.as_view(), name="calendar"),
    path("calendar/<int:year>/<int:month>/", views.calendar.as_view(), name="calendar"),
    path('medicine/<int:year>/<int:month>/<int:day>/', views.daily_medicine_detail.as_view(), name='medicine_sche'),  # You'll need to create this view
    path("patient/", views.PatientListView.as_view(), name="patient-list"),
    path('patient/<int:pk>/', views.PatientView.as_view(), name='patient-detail'),
    path("medicine/add/", views.MedicineAddView.as_view(), name="add-medicine"),
    path("medicine/edit/<int:pk>/", views.MedicineEditView.as_view(), name="edit-medicine"),
    path("medicine/delete/<int:pk>/", views.MedicineDeleteView.as_view(), name="delete-medicine"),
    path("daily-medicine/add/", views.DailyMedicineAddView.as_view(), name="add-daily-medicine"),
    path("daily-medicine/edit/<int:pk>/", views.DailyMedicineEditView.as_view(), name="edit-daily-medicine"),
    path("daily-medicine/delete/<int:pk>", views.DailyMedicineDeleteView.as_view(), name="delete-daily-medicine"),
    path('update-medicine-status/<int:medicine_id>/', views.update_medicine_status.as_view(), name='update_status'),

    path('side-effect/', views.side.as_view(), name='side-effect'),
    path('notification/', views.notification.as_view(), name='notification'),
    path('report/', views.report.as_view(), name='report'),
]
