from django.urls import path
from MEM_MED import views

urlpatterns = [
    path("medicine/", views.daily_medicine_detail.as_view(), name="show_course"),
    path("medicine/add/", views.MedicineAddView.as_view(), name="add-medicine"),
    path("medicine/edit/<int:pk>/", views.MedicineEditView.as_view(), name="edit-medicine"),
    path("medicine/delete/<int:pk>/", views.MedicineDeleteView.as_view(), name="delete-medicine"),
]
