from django.db import models


# Create your models here.
class Profile(models.Model):
    # profile_photo = models.ImageField(upload_to = 'profilepics/', default='Image')
    prof_pic = ImageField(blank=True, manual_crop='800x800')
    bio = HTMLField()
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


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Image(models.Model):
    image_path = models.ImageField(upload_to = 'images/')
    name = models.CharField(max_length=30)
    likes = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
   
    
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
    
    @classmethod
    def get_comments_by_images(cls, id):
        comments = Comments.objects.filter(image__pk = id)
