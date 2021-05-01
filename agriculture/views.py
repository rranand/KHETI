from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .form import upload_img, soil_fertilizer_form, crop_recommendations_form
from .models import weed_image, fields
from weed_checker import predict, soil_fertilizer_predict, crop_recommendations_predict
from Disease.frontenddisease import plant_disease_predict


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


def soil_fertilizer(request):
    f1 = soil_fertilizer_form()

    if request.method == 'POST':
        f1 = soil_fertilizer_form(request.POST)

        if f1.is_valid():
            t = float(f1.cleaned_data['temp'])
            h = float(f1.cleaned_data['humidity'])
            m = float(f1.cleaned_data['moisture'])
            s = f1.cleaned_data['soil']
            c = f1.cleaned_data['crop']
            n = float(f1.cleaned_data['nitrogen'])
            k = float(f1.cleaned_data['potassium'])
            p = float(f1.cleaned_data['phosphorus'])

            x = soil_fertilizer_predict(t, h, m, s, c, n, k, p)

            return render(request, 'soil_fertilizer.html', {'f1': f1, 'predict': x})

    return render(request, 'soil_fertilizer.html', {'f1': f1})


def crop_recommend(request):
    f1 = crop_recommendations_form()

    if request.method == 'POST':
        f1 = crop_recommendations_form(request.POST)

        if f1.is_valid():
            n = float(f1.cleaned_data['nitrogen'])
            k = float(f1.cleaned_data['potassium'])
            p = float(f1.cleaned_data['phosphorus'])
            t = float(f1.cleaned_data['temp'])
            h = float(f1.cleaned_data['humidity'])
            ph = float(f1.cleaned_data['ph'])
            rainfall = float(f1.cleaned_data['rainfall'])

            x = crop_recommendations_predict(n, k, p, t, h, ph, rainfall)

            return render(request, 'crop_recommendation.html', {'f1': f1, 'predict': x})

    return render(request, 'crop_recommendation.html', {'f1': f1})


def plant_disease(request):
    f1 = upload_img()

    if request.method == 'POST':
        f1 = upload_img(request.POST, request.FILES)

        if f1.is_valid():
            img = f1.cleaned_data['image']
            f = weed_image.objects.create(img=img)
            f.save()

            x = plant_disease_predict(str(img)).split('___')[1].replace('_', ' ')

            return render(request, 'plant_disease.html', context={'f1': f1, 'predict': x, 'flag': 'healthy' == x})

    return render(request, 'plant_disease.html', context={'f1': f1})
