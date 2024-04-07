from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home,name="home"),
    path('',views.login_view,name='login'),
    path('subscribe/',views.subscribe,name='subscribe'),
    path('create_newsletter/',views.create_newsletter,name='create_newsletter'),
    path('newsletter/<str:department_name>/', views.newsletter_by_department, name='newsletter_by_department'),
    path('newsletter/<str:department_name>/<str:newsletter_title>', views.newsletter_detail, name='newsletter_detail'),
    path('create_employee_spotlight/', views.create_employee_spotlight, name='create_employee_spotlight'),
    path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('create_event/', views.create_event, name='create_event'),
    path('accounts/', include('django.contrib.auth.urls')), 
]


