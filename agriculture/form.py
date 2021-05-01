from django import forms
from .models import fields


SOIL = (
    ('black', 'Black Soil'),
    ('clayey', 'Clay Soil'),
    ('loamy', 'Loam Soil'),
    ('red', 'Red Soil'),
    ('sandy', 'Sandy Soil'),
)

CROP = (
    ('barley', 'Barley'),
    ('cotton', 'Cotton'),
    ('ground nuts', 'Ground Nuts'),
    ('maize', 'Maize'),
    ('millets', 'Millets'),
    ('oil seeds', 'Oil Seeds'),
    ('paddy', 'Paddy'),
    ('pulses', 'Pulses'),
    ('sugarcane', 'Sugarcane'),
    ('tobacco', 'Tobacoo'),
    ('wheat', 'Wheat'),
)


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


class soil_fertilizer_form(forms.Form):
    temp = forms.DecimalField(required=True, label='Temperature (in Celcius)')
    humidity = forms.DecimalField(required=True)
    moisture = forms.DecimalField(required=True)
    soil = forms.ChoiceField(required=True, choices=SOIL)
    crop = forms.ChoiceField(required=True, choices=CROP)
    nitrogen = forms.DecimalField(required=True)
    potassium = forms.DecimalField(required=True)
    phosphorus = forms.DecimalField(required=True)

    def __init__(self, *args, **kwargs):
        super(soil_fertilizer_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class crop_recommendations_form(forms.Form):
    nitrogen = forms.DecimalField(required=True)
    potassium = forms.DecimalField(required=True)
    phosphorus = forms.DecimalField(required=True)
    temp = forms.DecimalField(required=True, label='Temperature (in Celcius)')
    humidity = forms.DecimalField(required=True)
    ph = forms.DecimalField(required=True)
    rainfall = forms.DecimalField(required=True)

    def __init__(self, *args, **kwargs):
        super(crop_recommendations_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
