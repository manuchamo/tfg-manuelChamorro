from django.urls import path
from logic import views

urlpatterns = [
    path('', views.index, name='landing'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('vote/', views.vote, name='vote'),
    path('myvotes/', views.myvotes, name='myvotes'),
]



