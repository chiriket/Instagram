from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='profile/')
    pub_date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles
    
    @classmethod
    def search_by_username(cls,search_term):
        profiles = cls.objects.filter(title__icontains=search_term)
        return profiles
    
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)

    def save_profile(self):
        self.save()
    
    @classmethod
    def search_profile(cls, name):
        profile = Profile.objects.filter(user__username__icontains = name)
        return profile
    
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile


# class Post(models.Model):
#     title = models.TextField()
#     cover = models.ImageField(upload_to='images/')

#     def __str__(self):
#         return self.title

class Image(models.Model):
    image_path = models.ImageField(upload_to = 'images/')
    name = models.CharField(max_length=30)
    likes = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)

    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
   )
   
    
    class Meta:
        ordering = ('-id',)

    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()
    
    def __str__(self):
        return self.name


class Comments(models.Model):
    comment = HTMLField()
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()
    
    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
