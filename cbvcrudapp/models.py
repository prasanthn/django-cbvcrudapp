from django.db import models
from django.core.urlresolvers import reverse_lazy


class Author(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('cbvcrudapp-author-details', kwargs={'pk': self.pk})


class Book(models.Model):
    title = models.CharField(max_length=256)

    author = models.ForeignKey(Author, related_name='books')

    def __unicode__(self):
        return self.title
