from django.db import models

class Laws(models.Model):
    law_name = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.name