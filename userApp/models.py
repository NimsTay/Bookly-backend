
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

# override the class that handles user creation like the manage.py createsuperuser command calls this class
class CustomUserManager(UserManager):

    #override
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("No email provided")
        #built in func to lowercase
        email = self.normalize_email(email)
        #create the a new auth user model
        user = self.model(email=email, **extra_fields)
        #call the built in func to hash the password
        user.set_password(password)
        #add user to db
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=False, default=None, unique=True, null=False)
    # first_name = models.CharField(max_length=48, null=False, blank=False)
    # last_name = models.CharField(max_length=48, null=True, blank=True)
    # phone = models.CharField(max_length=24, blank=False, unique=True, null=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    # birthday = models.DateField(blank=False, null=False)
    # city = models.TextField(null=False, blank=False)
    # state = models.TextField(null=False, blank=False)
    # country = models.CharField(max_length=4, null=False, blank=False)
    
    #overide the objects to use my custom user manager instead of base
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    #define metadata/configuration of class itself or settings for how django should disply model to admin
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    # def get_short_name(self):
        # return self.first_name
    
    # def get_full_name(self):
        # return self.first_name + ' ' + self.last_name