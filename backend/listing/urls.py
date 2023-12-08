from django.contrib import admin
from django.urls import path, include

from .views import ListingDetailView, ListingsView, ManageListingView

urlpatterns = [
    path('manage',ManageListingView.as_view()),
    path('detail',ListingDetailView.as_view()),
    path('get-listings',ListingsView.as_view()),
]


