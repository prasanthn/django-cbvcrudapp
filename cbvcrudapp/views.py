from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.forms.models import (modelform_factory, inlineformset_factory,
                                 modelformset_factory)
from django.shortcuts import redirect


class InlineObjectsForm(object):
    """Form for one main object and several "inline" objects.

    main_model: the main model
    main_model_fields: the fields of this model to use in a ModelForm
    inline_model: the model whose instances will be present inline
    inline_model_fields: the fields of the inline model to be added to forms

    initial: initial data passed to form constructors
    prefix: form prefix
    success_url: URL to redirect to after successfull processing of a form
    extra: number of empty inline forms to add

    """
    main_model = None
    main_model_fields = None
    inline_model = None
    inline_model_fields = None

    initial = {}
    prefix = None
    success_url = None
    extra = 1

    def get_success_url(self):
        if self.success_url:
            return self.success_url % self.object.__dict__
        else:
            return self.object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.initial,
            'prefix': self.prefix
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES
            })
        return kwargs

    def form_invalid(self, main_form, inline_forms):
        return self.render_to_response(
            self.get_context_data(main_form=main_form, inline_forms=inline_forms)
        )


class InlineObjectsCreateForm(InlineObjectsForm):
    """A form for creating a model and 'inline' models associated with it.

    Inherits InlineObjectsForm

    fk_field: the field in the main model that forms a reverse foreign-key to
              the inline models.

    """
    fk_field = None

    def get_form_classes(self):
        MainForm = modelform_factory(model=self.main_model, fields=self.main_model_fields)
        InlineForms = modelformset_factory(model=self.inline_model,
                                           fields=self.inline_model_fields,
                                           extra=self.extra)
        return MainForm, InlineForms

    def get_forms(self):
        MainForm, InlineForms = self.get_form_classes()
        kwargs = self.get_form_kwargs()

        return (MainForm(**kwargs),
                InlineForms(queryset=self.inline_model.objects.none(), **kwargs))

    def form_valid(self, main_form, inline_forms):
        self.object = main_form.save(commit=True)
        self.inline_objects = inline_forms.save(commit=False)
        setattr(self.object, self.fk_field, self.inline_objects)
        self.object.save()

        return redirect(self.get_success_url())


class InlineObjectsUpdateForm(InlineObjectsForm):
    """A form to update a model and 'inline' models associated with it.

    Inherits InlineObjectsForm.

    """
    def get_form_classes(self):
        MainForm = modelform_factory(model=self.main_model, fields=self.main_model_fields)
        InlineForms = inlineformset_factory(parent_model=self.main_model,
                                            model=self.inline_model,
                                            fields=self.inline_model_fields,
                                            extra=self.extra)
        return MainForm, InlineForms

    def get_form_kwargs(self):
        kwargs = super(InlineObjectsUpdateForm, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs

    def get_forms(self):
        MainForm, InlineForms = self.get_form_classes()
        kwargs = self.get_form_kwargs()

        return MainForm(**kwargs), InlineForms(**kwargs)

    def form_valid(self, main_form, inline_forms):
        self.object = main_form.save(commit=True)
        self.inline_objects = inline_forms.save(commit=True)

        return redirect(self.get_success_url())


class ProcessInlineObjectsFormView(View):
    """A partial view that processes an InlineObjectsForm."""
    def get(self, request, *args, **kwargs):
        main_form, inline_forms = self.get_forms()
        return self.render_to_response(
            self.get_context_data(main_form=main_form, inline_forms=inline_forms))

    def post(self, request, *args, **kwargs):
        main_form, inline_forms = self.get_forms()

        if main_form.is_valid() and inline_forms.is_valid():
            return self.form_valid(main_form=main_form, inline_forms=inline_forms)
        else:
            return self.form_invalid(main_form=main_form, inline_forms=inline_forms)


class InlineObjectsCreateView(ContextMixin, TemplateResponseMixin,
                              InlineObjectsCreateForm, ProcessInlineObjectsFormView):
    """View for creating a model and an inline model associted with it.

    Example usage:

    InlineObjectsCreateView.as_view(
        main_model=models.Author,
        main_model_fields=('name',),
        fk_field='books',
        inline_model=models.Book,
        inline_model_fields=('title',),
        success_url="/author/%(id)s/",
        template_name="author_create_with_books.html"
    )

    """
    def get(self, request, *args, **kwargs):
        self.object = None
        return super(InlineObjectsCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(InlineObjectsCreateView, self).post(request, *args, **kwargs)


class InlineObjectsUpdateView(SingleObjectMixin, TemplateResponseMixin,
                              InlineObjectsUpdateForm, ProcessInlineObjectsFormView):
    """View for updating a model and an inline model associated with it.

    Example usage:

    InlineObjectsUpdateView.as_view(
        main_model=models.Author,
        main_model_fields=('name',),
        inline_model=models.Book,
        inline_model_fields=('title',),
        success_url="/author/%(id)s/",
        template_name="author_update_with_books.html"
    )
    """
    def get_queryset(self):
        return self.main_model.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(InlineObjectsUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(InlineObjectsUpdateView, self).post(request, *args, **kwargs)
