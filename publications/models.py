from django.db import models
from django.contrib.auth import get_user_model
from core.models import Base
from stdimage.models import StdImageField

# Create your models here.

class PostManage():

    def sort_contents(self):
        return self.get_queryset().all().all().order_by("datetime_created")[0:30]


class Publication(Base):
    text = models.CharField(max_length=355)
    archive = models.FileField(upload_to='publications', blank=True)

    class Meta:
        verbose_name = 'publication'
        verbose_name_plural = "publications"


class Post(Publication):
    propertier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts"),
    visible = models.BooleanField(default=True)


class Comment(Publication):
    propertier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts"),

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class TypeReaction(Base):
    name = models.CharField(max_length=10)
    image = StdImageField("imagem", upload_to="reactions", blank=False)


class Reaction(Base):
    type_reaction = models.ForeignKey(TypeReaction, on_delete=models.CASCADE, related_name="type_reaction")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reaction"),
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reaction", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reaction", null=True)

