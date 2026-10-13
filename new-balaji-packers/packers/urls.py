from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),
    path('quote/', views.quote_view, name='quote'),
    path('book/', views.quote_view, name='book'),
    path('thanks/', views.thanks_view, name='thanks_default'),
    path('thanks/<str:booking_ref>/', views.thanks_view, name='thanks'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('submit-review/', views.submit_review_view, name='submit_review'),
    path('reviews/', views.reviews_list_view, name='reviews'),
]
