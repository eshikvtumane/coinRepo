from coins.models import Coins
#http://www.youtube.com/watch?v=B-n6_m66TmA
from haystack import indexes

class CoinsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)

    content_auto = indexes.EdgeNgramField(model_attr='coin_name')

    def get_model(self):
        return  Coins

    def index_queryset(self, using=None):
        return self.get_model().objects.all()