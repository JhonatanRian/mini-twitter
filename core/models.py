from re import U
from typing import List
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from stdimage.models import StdImageField

# Create your models here.

class PostManager(models.Manager):

    def sort_contents(self):
        return self.get_queryset().all().all().order_by("datetime_created")[0:30]


class UserManage():
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError("E-mail e senha são obrigatórios")

        email = self.normalize_email(email)
        user = self.model(email=email, username="", **extra_fields)
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
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        validators=[username_validator],
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(unique=True)
    fone = models.CharField(max_length=15)
    friends = models.ManyToManyField("CustomUser")
    photo = StdImageField("photo user", upload_to='users', blank=True)
    back_cover = StdImageField("back cover", upload_to='users', blank=True)
    about_me = models.CharField("about me", max_length=355, blank=True)
    slug = models.SlugField('Slug', max_length=150, blank=True, editable=False)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['username', 'fone']

    objects = UserManage()


class Base(models.Model):
    datetime_created = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Publication(Base):
    text = models.CharField(max_length=355)
    archive = models.FileField(upload_to='publications', blank=True)


class Post(Publication):
    propertier = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts"),
    visible = models.BooleanField(default=True)


class Comment(Publication):
    propertier = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts"),


class TypeReaction(Base):
    name = models.CharField(max_length=10)
    image = StdImageField("imagem", upload_to="reactions", blank=False)


class Reaction(Base):
    type_reaction = models.ForeignKey(TypeReaction, on_delete=models.CASCADE, related_name="type_reaction")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reaction"),
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reaction", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reaction", null=True)


class FriendRequest(Base):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_request_sender")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="friend_request_recipient")
    accept = models.BooleanField(default=False)


def user_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.username)


models.signals.pre_save.connect(user_pre_save, sender=CustomUser)
