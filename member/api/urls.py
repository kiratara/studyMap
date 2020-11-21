from django.urls import include, path
from rest_framework.routers import DefaultRouter

from member.api import views

router = DefaultRouter()
router.register('', views.MemberViewSet, basename="members")
# router.register('register/', views.MemberRegisterView, basename="members-register")


urlpatterns = [
    path('', include(router.urls)), # router creates a list of url mapping to each http actions api/users/[list, ...]
]