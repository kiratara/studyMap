from django.contrib.auth.models import PermissionsMixin, User
from django.db import models


# Create your models here.
class Topic(models.Model):
    """Describe topic model 
    This is the main over-arching topic containing subtopics
    """
    title = models.CharField(max_length=255)
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic')

    def __str__(self):
        """Retrieve string representation of Topic model"""
        return self.title


class SubTopic(models.Model):
    """Describe SubTopic model"""
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subtopics")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        """Return string representation of the SubTopic model"""
        return self.title


class Note(models.Model):
    """Define Notes a model class"""
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        """Return string representation of notes model"""
        return f"Note created for {self.subtopic}"
