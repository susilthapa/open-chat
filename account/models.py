from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("User must have an email address.")
        if not username:
            raise ValueError("User must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )   
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin=True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user


def get_profile_image_filepath(self, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'images/profile_images/{self.pk}/{filename}'

def get_default_profile_image():
    return 'images/logo_1080_1080.png'

class Account(AbstractBaseUser):
    email               = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username            = models.CharField(max_length=30, unique=True)
    date_joined         = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    hide_email          = models.BooleanField(default=True)
    profile_image       = models.ImageField(max_length=255,
                            upload_to=get_profile_image_filepath,
                            default=get_default_profile_image,
                            null=True,
                            blank=True
                            )

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # def get_profile_image_filename(self):
    #     return str(self.profile_image)[str(self.profile_image).index(f'images/profile_images/{self.pk}'):]

    def has_perm(self, perm, object=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True