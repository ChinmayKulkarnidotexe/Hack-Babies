from django.db import models

class Laws(models.Model):
    title = models.CharField(max_length=500)
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.name