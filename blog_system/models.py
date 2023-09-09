from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
# Create your models here.


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    content = models.TextField(max_length=255)
    number_of_views = models.IntegerField(default=0)
    cover_photo = models.ImageField(upload_to="post_covers/", null=True, blank=True)

    def __str__(self):
        return self.title


# this post comment manager ensures that the parent of a comment belongs to the same post of the child comment


class PostComment(models.Model):
    def save(self, *args, **kwargs):
        if self.parent_comment_id and self.parent_comment_id.post_id != self.post_id:
            raise ValidationError("Parent comment does not belong to the same post.")
        super(PostComment, self).save(*args, **kwargs)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment_id = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    content = models.TextField(max_length=255)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return "comment" + str(self.user_id) + ":" + str(self.post_id)


class LikePost(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id) + ":" + str(self.post_id)

    class Meta:
        unique_together = ("post_id", "user_id")
