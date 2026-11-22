
from django.db import models
from accounts.models import Company


class Job(models.Model):

    JOB_TYPE = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    skills_required = models.TextField()

    location = models.CharField(max_length=100)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE,
        default='Full Time'
    )

    posted_date = models.DateTimeField(auto_now_add=True)

    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
