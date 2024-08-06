"""
URL configuration for serveur project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from service.views import  LoginRegisterView, SpecialiteListView, CycleListView, payement_data, SpecialitesByFormationView
from service.views import VilleListView, FormationListView

urlpatterns = [
    path('admin', admin.site.urls),
    path('auth/', LoginRegisterView.as_view(), name='auth'),
    path('villes/', VilleListView.as_view(), name='ville-list'),
    path('formations/', FormationListView.as_view(), name='formation-list'),
    path('specialites_list/', SpecialiteListView.as_view(), name='specilite-list'),
    path('cycles/', CycleListView.as_view(), name='cycle-list'),
    path('payement/', payement_data, name='payment_data'),
    path('specialites/<int:formation_id>/<int:specialite_id>/<int:ville_id>', SpecialitesByFormationView.as_view(), name='specialites-by-formation'),
]
