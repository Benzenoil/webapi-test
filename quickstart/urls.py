from django.urls import include, path
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.rest_signup, name='rest-signup'),
    path('users/<str:pid>/', views.rest_getuser_detail, name='rest_getuser_detail'),
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
]
