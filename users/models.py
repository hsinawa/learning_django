from django.db import models

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=150,)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    permissions = models.JSONField(default=list) 
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    def get_email_field_name(self):
        return f"{self.email}"