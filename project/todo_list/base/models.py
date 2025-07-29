from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os

def user_directory_path(instance, filename):
    # Files uploaded to MEDIA_ROOT/user_<id>/task_<id>/<filename>
    return f'user_{instance.task.user.id}/task_{instance.task.id}/{filename}'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    reminder_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

def delete(self, *args, **kwargs):
    if self.complete:
        super().delete(*args, **kwargs)
    else:
        raise ValidationError("Cannot delete an incomplete task.")


class TaskMedia(models.Model):
    task = models.ForeignKey(Task, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'docx', 'txt'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.filename()
