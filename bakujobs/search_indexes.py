from bakujobs.models import Job
from haystack import indexes
import datetime

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text            = indexes.CharField(document=True, use_template=True)
    title           = indexes.CharField(model_attr='job_title')
    slug            = indexes.CharField(model_attr='slug')

    def get_model(self):
        return Job

    def index_queryset(self, using=None):
        return self.get_model().objects.all()