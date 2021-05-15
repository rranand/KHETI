import io
import torch
from torchvision import transforms
from PIL import Image
from .utils.model import ResNet9
from io import BytesIO
from django.conf import settings


def plant_disease_predict(dire=""):
    path = settings.BASE_DIR / dire
    disease_classes = ['Apple___Apple_scab',
                       'Apple___Black_rot',
                       'Apple___Cedar_apple_rust',
                       'Apple___healthy',
                       'Blueberry___healthy',
                       'Cherry_(including_sour)___Powdery_mildew',
                       'Cherry_(including_sour)___healthy',
                       'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                       'Corn_(maize)___Common_rust_',
                       'Corn_(maize)___Northern_Leaf_Blight',
                       'Corn_(maize)___healthy',
                       'Grape___Black_rot',
                       'Grape___Esca_(Black_Measles)',
                       'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                       'Grape___healthy',
                       'Orange___Haunglongbing_(Citrus_greening)',
                       'Peach___Bacterial_spot',
                       'Peach___healthy',
                       'Pepper,_bell___Bacterial_spot',
                       'Pepper,_bell___healthy',
                       'Potato___Early_blight',
                       'Potato___Late_blight',
                       'Potato___healthy',
                       'Raspberry___healthy',
                       'Soybean___healthy',
                       'Squash___Powdery_mildew',
                       'Strawberry___Leaf_scorch',
                       'Strawberry___healthy',
                       'Tomato___Bacterial_spot',
                       'Tomato___Early_blight',
                       'Tomato___Late_blight',
                       'Tomato___Leaf_Mold',
                       'Tomato___Septoria_leaf_spot',
                       'Tomato___Spider_mites Two-spotted_spider_mite',
                       'Tomato___Target_Spot',
                       'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                       'Tomato___Tomato_mosaic_virus',
                       'Tomato___healthy']

    disease_model_path = settings.BASE_DIR / 'Disease' / 'utils' / 'plant_disease_model.pth'
    disease_model = ResNet9(3, len(disease_classes))
    disease_model.load_state_dict(torch.load(disease_model_path, map_location=torch.device('cpu')))
    disease_model.eval()

    file = Image.open(path)
    # Create a buffer to hold the bytes
    buf = BytesIO()

    # Save the image as jpeg to the buffer
    file.save(buf, 'jpeg')

    # Rewind the buffer's file pointer
    buf.seek(0)

    # Read the bytes from the buffer
    img = buf.read()

    # Close the buffer
    buf.close()

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])

    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)

    yb = disease_model(img_u)

    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]

    treatment = {'Tomato___Late_blight': "Spray Dimethomorph@1.0%+Polyram@0.2% weekly",
                 'Corn_(maize)___Northern_Leaf_Blight': "Spray Tebuconazole fungicide weekly ",
                 'Tomato___Early_blight': "Spray Azoxystrobin+ Tebuconazole(1ml/L) with spreading agent Nagastha(25ml/L) in evening hours",
                 'Tomato___Septoria_leaf_spot': "Use Carbendazim 50% SC fungicide ",
                 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': "Spray Mancozeb 75% WP, 80% WP fungicide",
                 'Strawberry___Leaf_scorch': "Spray CHLOROTHALONIL 75% WP fungicide",
                 'Apple___Apple_scab': "Use Mancozeb75%WP with a concentration of 30gm/litre 10Lt/tree ",
                 'Tomato___Bacterial_spot': "Use Copper Oxychloride 50% WP with 750ml/1000 dilution",
                 'Apple___Black_rot': "Spray MANCOZEB 75% WP, 80% WP fungicide",
                 'Cherry_(including_sour)___Powdery_mildew': "Use 2-5Ltr/ha Lime Sulphur 22% SC",
                 'Peach___Bacterial_spot': "Spray SULFUR 80% WP, 80% WG fungicide",
                 'Apple___Cedar_apple_rust': "Spray MANCOZEB 75% WP, 80% WP fungicide",
                 'Tomato___Target_Spot': "Use Copper Oxychloride 50% WP with 750ml/1000 dilution",
                 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': "Spraying of fungicides- Captan (0.2%), aureofungin (500 ppm.), DCNA (2,6-dicholoro-4-nitroaniline)-0.2%",
                 'Potato___Late_blight': "Use MetalaxylM4%+ Mancozeb64%WP with 2.5% formulation at an interval of 24 days till harvest",
                 'Tomato___Tomato_mosaic_virus': "Use 100 g of micronutrient fertilizers are added per liter of milk whey also apply potassium permanaganate solution to soil cover after removing infected plants",
                 'Grape___Black_rot': "Use Captan 50% WP fungicide spray",
                 'Potato___Early_blight': "Use Captan 50% WP fungicide spray",
                 'Corn_(maize)___Common_rust_': "Spray 1g/ml formulated Azoxystrobin 18.2% w/w + Cyproconazole 7.3% w/w SC fungicide spray",
                 'Pepper,_bell___Bacterial_spot': "Use CHLOROTHALONIL 75% WP fungicide spray"}

    try:
        x = treatment[prediction]
    except KeyError:
        x = ''

    return [prediction, x]


