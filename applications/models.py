
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(
        upload_to='applications/resumes/'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    applied_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'job'],
                name='unique_student_job_application'
            )
        ]

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"

resume = models.FileField(
    upload_to='applications/resumes/',
    blank=True,
    null=True
)