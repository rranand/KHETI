from django import forms
from django.forms import formset_factory

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


class upload_img_only(forms.Form):
    image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super(upload_img_only, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class upload_two_image(forms.Form):
    img_1 = forms.ImageField(label='Red Band Image', required=True)
    img_2 = forms.ImageField(label='Infrared Image', required=True)

    def __init__(self, *args, **kwargs):
        super(upload_two_image, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class upload_img(forms.Form):
    image = forms.ImageField(required=True)
    ordinates = forms.CharField(label='Co-Ordinates', help_text='Example: \"25.0#12.0 27.0#13.0 28.4#58.45 25.0#12.0\"')

    def __init__(self, *args, **kwargs):
        super(upload_img, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


upload_img_set = formset_factory(upload_img, extra=1)


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
