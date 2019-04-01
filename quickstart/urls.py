from django.urls import include, path
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
# ]

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', views.rest_users, name='rest-users'),
    path('signup/', views.rest_signup, name='rest-signup'),
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),
]
