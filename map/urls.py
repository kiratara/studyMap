from django.urls import include, path
from rest_framework.routers import DefaultRouter

from map import views


router = DefaultRouter()
# register the users route, does not require the / as router will create it
router.register('topics', views.TopicViewSet)
router.register('subTopics', views.SubTopicViewSet)
router.register('notes', views.NoteViewSet)

urlpatterns = [
    path('', include(router.urls)), # router creates a list of url mapping to each http actions api/users/[list, ...]
]
