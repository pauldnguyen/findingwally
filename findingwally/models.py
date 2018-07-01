from django.db import models

class URLImage(models.Model):
    url = models.URLField(max_length=2048)

    def __str__(self):
        return self.url
