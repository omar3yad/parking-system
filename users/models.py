from django.contrib.auth.models import AbstractUser
from django.db import models

# ----------------------------
# Custom User
# ----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # لتجنب أي تصادم مع auth.User الافتراضي
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# ----------------------------
# Cars المملوكة للمستخدم
# ----------------------------
class Car(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    car_type = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plate_number
