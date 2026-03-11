from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.patients, name="patients"),
    path('doctors/', views.doctors, name='doctors'),
    path('nures/', views.nures, name='nures'),
    path('drugs/', views.drugs, name='drugs'),
    
    path('update_drug/<int:id>/', views.update_drug, name='update_drug'),
    path('update_doctor/<int:id>/', views.update_doctor, name='update_doctor'),
    path('update_nures/<int:id>',views.update_nures,name="update_nures"),
    path('update_patient/<int:id>/', views.update_patient, name='update_patient'),
    
    path('delete/<str:model>/<int:id>/', views.delete_item, name='delete_item'),
    
    
    
    
]