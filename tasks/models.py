from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(user_name=user_name ,email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(user_name=user_name, email=email, password=password, **extra_fields)

    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('team_lead', 'Team Lead'),
        ('member', 'Member'),
    )
    user_name = models.CharField(max_length=150, unique=True, blank=True) 
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email','first_name', 'last_name']

    def __str__(self):
        return self.email

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    members = models.ManyToManyField('CustomUser', related_name='teams', blank=True)
    team_lead = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='team_leads', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    

class Task(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'In Progress'),
        (2, 'Complete'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='tasks_assigned_to')
    assigned_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='tasks_assigned_by', blank=True, null=True)  
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0) 
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.assigned_by and self.assigned_by.role != 'team_lead':  
            raise ValueError("Only Team Leads can assign tasks.")
        super().save(*args, **kwargs)