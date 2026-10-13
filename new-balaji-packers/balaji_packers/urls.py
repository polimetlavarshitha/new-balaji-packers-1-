"""
URL configuration for New Balaji Packers and Movers project.
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "New Balaji Packers and Movers - Admin Portal"
admin.site.site_title = "New Balaji Packers Admin"
admin.site.index_title = "Branch Logistics, Booking Orders & Reviews"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('packers.urls')),
]
