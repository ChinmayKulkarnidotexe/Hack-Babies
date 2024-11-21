# models.py
import json
from django.db import models

# class Article(models.Model):
#     article = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     embedding = models.TextField()  # Store the list as a JSON string

#     def save(self, *args, **kwargs):
#         # Convert the list (embedding) to a JSON string before saving
#         if isinstance(self.embedding, list):
#             self.embedding = json.dumps(self.embedding)
#         super().save(*args, **kwargs)

#     def get_embedding(self):
#         # Convert the JSON string back to a list
#         return json.loads(self.embedding)



# class Article(models.Model):
#     article = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     embedding = ArrayField(models.FloatField(), blank=True)
#     # embedding = models.TextField()
#     def save(self, *args, **kwargs):
#         if not self.embedding:
#             self.embedding = get_article_embedding(self.description)
#         super().save(*args, **kwargs)


# class Article(models.Model):
#     name = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.title


# class Laws(models.Model):
#     law_name = models.CharField(max_length=100)
#     title = models.CharField(max_length=500)
#     desc = models.CharField(max_length=500)
#     def __str__(self):
#         return self.name