from django.contrib.auth.models import User
from django.db import models

default_image_path = 'images/default.jpg'


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='', default='no.gif')
    participation = models.ManyToManyField(User)

    def __str__(self):
        return "Id=%d, Name=%s, author=%s, description=%s"\
            % (self.id, self.name, self.author, self.description)
