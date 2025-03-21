from django.urls import path
from . import views

urlpatterns = [
    path('new_income/', views.new_income, name='new_income'),
    path('add_income/', views.add_income, name='add_income'),  # Make sure this exists
    path('new_expense/', views.new_expense, name='new_expense'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),

]
