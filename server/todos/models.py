from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=20, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  