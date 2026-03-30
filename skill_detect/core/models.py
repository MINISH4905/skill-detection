from django.contrib.auth.models import AbstractUser
from django.db import models


# ----------------------------
# DOMAIN MODEL
# ----------------------------
class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name
    

class TopicVersion(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.domain.name} - V{self.version_number}"
    
class DynamicTopic(models.Model):
    topic_version = models.ForeignKey(TopicVersion, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=20)
    industry_relevance = models.FloatField()

    def __str__(self):
        return self.title
    
from django.conf import settings

class UserCurriculum(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="curriculums"
    )
    topic_version = models.ForeignKey(
        TopicVersion,
        on_delete=models.CASCADE,
        related_name="user_curriculums"
    )
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic_version')  # Prevent duplicate assignment

    def __str__(self):
        return f"{self.user} - {self.topic_version}"


# ----------------------------
# CUSTOM USER MODEL
# ----------------------------
class User(AbstractUser):

    ROLE_CHOICES = (
        ('learner', 'Learner'),
        ('dev', 'Developer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='learner'
    )

    # ⭐ NEW FIELD → Domain Selection
    selected_domains = models.ManyToManyField(
        Domain,
        blank=True,
        related_name="users"
    )

    def __str__(self):
        return self.username