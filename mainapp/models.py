from django.db import models

# Create your models here.
class Template(models.Model):
    temp_name = models.CharField(max_length=200)
    temp_description = models.TextField()
    temp_text = models.TextField()
    def __str__(self):
        return self.temp_text
