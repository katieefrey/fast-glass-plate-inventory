from django.db import models
#from djongo import models

# Create your models here.

class Repository(models.Model):
    abbr = models.CharField(max_length=500)
    name = models.CharField(max_length=500, null=True)
    url = models.CharField(max_length=500, null=True)
    desc = models.TextField(null=True)
    #fields = models.ArrayField(null=True, model_container=ArchiveField)

    def __str__(self):
        return f"{self.name}"


# from mongoengine import Document, fields

# class GlassPlates(Document):
#     identifier = fields.StringField(required=True)
#     repository = fields.StringField(required=True)
#     exposure_info = fields.ListField()
#     obs_info = fields.DictField()
#     plate_info = fields.DictField()
