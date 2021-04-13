from django.shortcuts import render
from .form import upload_img
from .models import weed_image
from weed_checker import predict
from django.conf import settings
import os


def home(request):
    return render(request, "home.html")


def weed_r(request):
    f1 = upload_img()

    if request.method == 'POST':
        f1 = upload_img(request.POST, request.FILES)

        if f1.is_valid():
            img = f1.cleaned_data['image']
            f = weed_image.objects.create(img=img)
            f.save()
            flag = predict(str(img))
            os.remove(settings.BASE_DIR / str(f.img.name))

            if flag:
                return render(request, 'weed.html', context={'form': f1, 'present': 'a'})
            else:
                return render(request, 'weed.html', context={'form': f1, 'present': 'b'})

    return render(request, 'weed.html', context={'form': f1})
