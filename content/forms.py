from django import forms
from django_select2.forms import ModelSelect2Widget

from content.models import Content, Author
from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContentForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and editing content objects
    """

    class Meta:
        model = Content
        exclude = ['is_active', 'views_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['paid_only'].widget.attrs.update({'class': 'form-check-input'})


class AuthorForm(StyleFormMixin, forms.ModelForm):
    """
    Form for creating and editing author objects
    """

    class Meta:
        model = Author
        fields = '__all__'
