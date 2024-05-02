from collections import OrderedDict

from django import forms

from content.models import Content, Author, Report


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
        exclude = ['is_active', 'views_count', 'author', 'slug', 'num_reports']

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


class ReportForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'comment', 'screenshots']

    def __init__(self, content_info=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if content_info:
            self.fields['content_info'] = forms.CharField(label='Content to report', initial=content_info, widget=forms.TextInput(attrs={'readonly': True}))
            self.fields['content_info'].widget.attrs['value'] = content_info
            self.fields['content_info'].widget.attrs['readonly'] = True

    def order_fields(self, field_order):
        """Order form fields as specified in the field_order list."""
        if field_order:
            ordered_fields = OrderedDict((key, self.fields[key]) for key in field_order if key in self.fields)
            self.fields = ordered_fields


