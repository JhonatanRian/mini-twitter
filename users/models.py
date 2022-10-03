from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from stdimage.models import StdImageField
from typing import List
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from core.models import Base


class UserManage(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError("E-mail e senha são obrigatórios")

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser precisa ser True")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("staff precisa ser True")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    fone = models.CharField(max_length=15)
    friends = models.ManyToManyField("CustomUser")
    photo = StdImageField("photo user", upload_to='users', blank=True)
    back_cover = StdImageField("back cover", upload_to='users', blank=True)
    about_me = models.CharField("about me", max_length=355, blank=True)
    slug = models.SlugField('Slug', max_length=150, blank=True, editable=False)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['name',]

    objects = UserManage()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class FriendRequest(Base):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="friend_request_sender")
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="friend_request_recipient")
    accept = models.BooleanField(default=False)


def user_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.username)


models.signals.pre_save.connect(user_pre_save, sender=get_user_model())
