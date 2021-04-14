from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .form import upload_img
from .models import weed_image, fields
from weed_checker import predict


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

            if flag:
                return render(request, 'weed.html', context={'form': f1, 'present': 'a'})
            else:
                return render(request, 'weed.html', context={'form': f1, 'present': 'b'})

    return render(request, 'weed.html', context={'form': f1})


def get_location(request):
    response_data = {'data': None}
    location = get_object_or_404(fields, name=request.GET['name'])

    response_data['data'] = {
        'polygons': location.location.geojson,
        'title': location.name
    }

    return JsonResponse(response_data)
