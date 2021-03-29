from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class User(AbstractUser):
    light_color = models.CharField(max_length=20, null=True)
    dark_color = models.CharField(max_length=20, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag_user")
    color = models.CharField(max_length=7, validators=[MinLengthValidator(4)])

    def serialize(self):
        return {
            "name": self.name,
            "color": self.color
        }

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="task_user")
    title = models.CharField(max_length=80)
    date = models.DateField()
    tag = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)
    done = models.BooleanField(default=False)
    label = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)


    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "title": self.title,
            "date": self.date,
            "tag": self.tag,
            "description": self.description,
            "done": self.done
        }

    def __str__(self):
        return self.title

class SharedTask(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="shared_task")
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} => {self.recipient}: ({self.task.title})"

class Friend(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requester")
    requestee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requestee")
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester} => {self.requestee}"