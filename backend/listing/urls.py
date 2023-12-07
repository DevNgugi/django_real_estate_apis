from django.contrib import admin
from django.urls import path, include

from .views import ManageListingView

urlpatterns = [
    path('manage',ManageListingView.as_view()),
    # path('manage',ManageListingView.as_view()),
    
    
]


