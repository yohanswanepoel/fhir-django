# myapp/urls.py
from django.urls import path
from .views import index, patient_detail

urlpatterns = [
    path('', index, name='index'),
    path('patient/<int:patient_id>/', patient_detail, name='patient_detail'),
]
