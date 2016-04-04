# from csvImporter.model import CsvModel
from django.db import models
import sys
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)



class MyList:

   def index(self):
       return 0

# class MyCsvModel(CsvModel):
    # all_university_names = CharField()

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()

class Data:

    @staticmethod
    def get_time_data(self):
        timesData = pd.read_csv("resources/data/timesData.csv")
        return  timesData

    @staticmethod
    def get_shanghai_data(self):
        shanghaiData = pd.read_csv("resources/data/shanghaiData.csv")
        return shanghaiData

    @staticmethod
    def get_cwur_data(self):
        cwurData = pd.read_csv("resources/data/cwurData.csv")
        return cwurData