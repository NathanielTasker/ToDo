from django.db import models
from django.utils import timezone


class Task(models.Model):
    task_text = models.CharField(max_length=60)
    pub_date = models.DateTimeField('date published')
    deadline = models.DateTimeField(null=True)
    completion_date = models.DateTimeField(null=True)
    finishing = models.BooleanField(default=False)

    def __str__(self):
        return self.task_text

    def is_past_deadline(self):
        if self.deadline:
            return self.deadline < timezone.now()
