""" Signal methods : Notes for my future self when I visit and I've mostly forgotten why and how this exists

REASON: When a new user is created, also create an new instance of studyRoom for the user
Whenever a new user instance is "saved", a signal is sent and a function with the
@reciever decorator is going to receive that signal
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_study_room(sender, instance, created, **kwargs):
    """A function that listens for a signal when a User's "save" method is called

    It checks if the save was called to create a new User instance or update an existing one
    If a new user is created then this method also creates a new instance of StudyRoom model
    associated to the current new user. 
    Also creates associated default child models
    
    """
    # created value is True if a new user was created
    if created:
        token = Token.objects.create(user=instance)
        # create a new StudyRoom instance whose user value is current User isntance
        # study_room = StudyRoom.objects.create(user=instance)
        # for topic, subtopics in default_data.items():
        #     #create topics
        #     topic = Topic.objects.create(title=topic, study_room=study_room)
        #     for subtopic in subtopics:
        #         SubTopic.objects.create(title=subtopic, topic=topic)
