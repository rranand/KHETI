from django import forms
from .models import fields


class upload_img(forms.Form):
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(upload_img, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class FieldsForm(forms.ModelForm):
    class Meta:
        model = fields
        fields = ('name', 'location')
