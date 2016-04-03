# from csvImporter.model import CsvModel
from django.db import models
from django.forms import CharField
from django.core.management.base import BaseCommand, CommandError
import csv
import csvImporter



class MyList:

   def index(self):
       return 0

# class MyCsvModel(CsvModel):
    # all_university_names = CharField()

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()