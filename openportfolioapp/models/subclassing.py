from django.db.models.query import QuerySet
from django.db import models
import pandas as ps
from pandas.core.datetools import MonthEnd
import numpy as np



class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()
            
            

        

