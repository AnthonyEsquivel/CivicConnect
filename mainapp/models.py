from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    temp_name = models.CharField(max_length=200)
    temp_description = models.TextField()
    temp_text = models.TextField()
    tags = models.ManyToManyField(Tags)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    public = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.temp_text


# extend a class so the user can have other fields added and stored
class MyUser(models.Model):
    address = models.CharField(max_length=1000)
    member_since = models.DateTimeField()
    # get django defined user model, creates a one to one w this user
    # if you delete the django user, delete my user too
    user = models.OneToOneField(User, default=0, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()



