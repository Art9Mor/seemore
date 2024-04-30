from django import forms

from content.models import Content, Author


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
        exclude = ['is_active', 'views_count', 'author', 'slug']

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
