from django.urls import path
from MEM_MED import views

urlpatterns = [
    path("", views.calendar.as_view(), name="calendar"),
    path("calendar/<int:year>/<int:month>/", views.calendar.as_view(), name="calendar"),
    path('medicine/<int:year>/<int:month>/<int:day>/', views.daily_medicine_detail.as_view(), name='medicine_sche'),  # You'll need to create this view
    path("medicine/add/", views.MedicineAddView.as_view(), name="add-medicine"),
    path("medicine/edit/<int:pk>/", views.MedicineEditView.as_view(), name="edit-medicine"),
    path("medicine/delete/<int:pk>/", views.MedicineDeleteView.as_view(), name="delete-medicine"),
    path('update-medicine-status/<int:medicine_id>/', views.update_medicine_status.as_view(), name='update_status'),
    path('patient/<int:pk>/', views.PatientView.as_view(), name='patient-detail'),

]
