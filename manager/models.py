from django.db import models
from django.contrib.auth import get_user_model



User = get_user_model()
# Create your models here.
class ManagerProfile(models.Model):
    REGION_CHOICES = (
    ('AHAFO', 'AHAFO'),
    ('ASHANTI', 'ASHANTI'),
    ('BONO & BONO EAST', 'BONO & BONO EAST'),
    ('CENTRAL', 'CENTRAL'),
    ('EASTERN', 'EASTERN'),
    ('GREATER ACCRA', 'GREATER ACCRA'),
    ('HEAD OFFICE', 'HEAD OFFICE'),
    ('NORTHERN', 'NORTHERN'),
    ('UPPER EAST', 'UPPER EAST'),
    ('WESTERN', 'WESTERN'),
    ('Greater Accra', 'Greater Accra'),
    ('WESTERN NORTH', 'WESTERN NORTH'),
)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    region = models.CharField(max_length=50, choices=REGION_CHOICES)

    def save(self, *args, **kwargs):
        if self.user.role != "Manager":
            raise ValueError("Only managers can have a ManagerProfile")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.region}"








        