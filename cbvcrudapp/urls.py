from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView, DeleteView
from django.core.urlresolvers import reverse_lazy

from . import models, views

urlpatterns = patterns(
    "",
    url(r'^authors/$',
        ListView.as_view(model=models.Author),
        name='cbvcrudapp-authors'),
    url(r'^author/(?P<pk>\d+)/$',
        DetailView.as_view(model=models.Author),
        name='cbvcrudapp-author-details'),
    url(r'^author/create/$',
        views.InlineObjectsCreateView.as_view(
            main_model=models.Author,
            main_model_fields=('name',),
            fk_field='books',
            inline_model=models.Book,
            inline_model_fields=('title',),
            template_name='cbvcrudapp/author_create_with_books.html'),
        name='cbvcrudapp-author-create'),
    url(r'^author/update/(?P<pk>\d+)/$',
        views.InlineObjectsUpdateView.as_view(
            main_model=models.Author,
            main_model_fields=('name',),
            inline_model=models.Book,
            inline_model_fields=('title',),
            template_name='cbvcrudapp/author_update_with_books.html'),
        name='cbvcrudapp-author-update'),
    url(r'^author/delete/(?P<pk>\d+)/$',
        DeleteView.as_view(model=models.Author,
                           success_url=reverse_lazy('cbvcrudapp-authors')),
        name='cbvcrudapp-author-delete')
)
