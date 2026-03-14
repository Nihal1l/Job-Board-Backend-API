from django.db import models
from django.conf import settings
from job_seeker.models import appliedJobs

class ChatRoom(models.Model):
    application = models.ForeignKey(appliedJobs, on_delete=models.CASCADE, related_name='chat_rooms')
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_chat_rooms')
    job_seeker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_seeker_chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('application', 'employer', 'job_seeker')

    def __str__(self):
        return f"Chat for {self.application.job.title} - {self.job_seeker.email}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Msg from {self.sender.email} at {self.timestamp}"
