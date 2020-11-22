from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_views

from member.api import views

router = DefaultRouter()
# router.register('', views.MemberViewSet, basename="members")
# router.register('register/', views.MemberRegisterView, basename="members-register")


urlpatterns = [
    path('register/', views.MemberRegisterView.as_view()),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api-token-auth'),
    path('<pk>/', views.MemberRetrieveUpdateDestroyAPIView.as_view()),
    path('', views.MemberLisAPIView.as_view()),

    # path('api-token-auth/', token_views.obtain_auth_token, name='api-token-auth'),
    # path('', include(router.urls)), # router creates a list of url mapping to each http actions api/users/[list, ...]
]