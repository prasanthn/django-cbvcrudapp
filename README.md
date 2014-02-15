# A Django CRUD app using Class Based Views

This repo is a demo of a CRUD app using Django's class based views.

Look at ``cbvcrudapp.urls`` too see how the views are setup.

The module ``cbvcrudapp.views`` contains the views ``InlineObjectsCreateView``
and ``InlineObjectsUpdateView`` that allow us to simulatneously update a model
and instances of another model that has a foreign key pointing to it.

The templates in ``cbvcrudapp/templates`` has JavaScript embedded in them that
will properly handle Django's formsets.

I have run this code using Django 1.6 and Python 2.7.
