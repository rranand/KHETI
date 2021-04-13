from django import forms


class upload_img(forms.Form):
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(upload_img, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
