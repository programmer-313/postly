import uuid

from django.db import models
from  django.contrib.auth import get_user_model

from cloudinary.models import CloudinaryField


User = get_user_model()


# create base abstract model with uuid as pk
class BaseUUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    class Meta:
        abstract = True 


class PostTag(BaseUUIDModel):
    keyword = models.SlugField(unique=True, max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class Post(BaseUUIDModel):
    post_title = models.CharField(max_length=200)
    posted_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="posts",
    )
    post_content = models.TextField(blank=True)
    post_views = models.PositiveBigIntegerField(default=0)
    post_like_count = models.PositiveBigIntegerField(default=0)
    post_dislike_count = models.PositiveBigIntegerField(default=0)
    tags = models.ManyToManyField(PostTag)
    posted_at = models.DateTimeField(auto_now_add=True)
    post_edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_title
    

class PostImage(BaseUUIDModel):
    image = CloudinaryField("post_image", folder="post_images/")
    index = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_images",   
    )
    
    def __str__(self):
        return f"{self.post}'s image of index {self.index}"

class PostComment(BaseUUIDModel):
    comment_content = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments" 
    )
    commented_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"         
    )
    commented_at = models.DateTimeField(auto_now_add=True)
    comment_edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commented_by}'s comment on {self.post}"
    

class PostLike(BaseUUIDModel):
    is_liked = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_likes"   
    )
    reacted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_likes"   
    )
    def __str__(self):
        return f"{self.reacted_by}'s like status on {self.post}"
    

class PostDislike(BaseUUIDModel):
    is_disliked = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_dislikes"   
    )
    reacted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_dislikes"   
    )
    def __str__(self):
        return f"{self.reacted_by}'s dislike status on {self.post}"
