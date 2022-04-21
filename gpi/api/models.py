# from django.db import models
# from django.conf import settings


# class Item(models.Model):
#     title = models.CharField(max_length=50)
#     description = models.TextField()
#     owner = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
#     )

# from mongoengine import Document, EmbeddedDocument, fields

# class Plate(models.Model):
#     identifier = models.CharField(max_length=100)
#     archive = models.CharField(max_length=100)
#     plate_info = fields.DictField()
#     obs_info = fields.DictField()
#     exposure_info = fields.ListField()
    
    
