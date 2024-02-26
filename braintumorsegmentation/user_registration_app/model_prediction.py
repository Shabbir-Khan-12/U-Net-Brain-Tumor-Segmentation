import cv2, numpy as np, keras
from keras.models import load_model
from .dice_func import dice_coefficient_loss, dice_coefficients, iou
import matplotlib.pyplot as plt
from PIL import Image
import os, io, glob
from django.conf import settings
import uuid
import base64

plt.style.use("ggplot")


class ModelPrediction:
    def __init__(self, image):
        self.image = image.read()
        self.__model : keras.Model = load_model(
            r"D:\FYP2\U-Net Brain Tumor Segmentation\braintumorsegmentation\user_registration_app\unet.hdf",
            custom_objects={
                "dice_coefficient_loss": dice_coefficient_loss,
                "iou": iou,
                "dice_coefficients": dice_coefficients,
            },
        )
        self.__image_height = 256
        self.__image_width = 256

    def getPrediction(self):
        nparr = np.frombuffer(self.image, np.uint8)

        # Decode the image using OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (self.__image_height, self.__image_width))

        img = img/255
        img = img[np.newaxis, :, :, : ]

        predicted_img = self.__model.predict(img)

        # Assuming predicted_image is your NumPy array
        predicted_img = predicted_img.squeeze()  # Remove the extra dimension
        predicted_img = (predicted_img * 255).astype(np.uint8)

        plt.imshow(predicted_img, interpolation='nearest')
        image = Image.fromarray(predicted_img)
        image_data = image.convert('RGB').tobytes

        # Save image to media storage
        image_path = f"\images\{uuid.uuid4()}.png"

        # # Use glob to find all .png files in the directory
        # png_files = glob.glob(os.path.join(f'{settings.ML_MODEL_LOCATION}/images' , '*.png'))

        # # Loop through the list of .png files and remove each one
        # for file_path in png_files:
        #     try:
        #         os.remove(file_path)
        #         print(f"Deleted {file_path}")
        #     except Exception as e:
        #         print(f"Error deleting {file_path}: {e}")
                
        image.save(settings.MEDIA_ROOT + image_path)
        context = {"image_url": settings.MEDIA_ROOT + image_path}

        with open(context['image_url'], "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        ctx = {}
        ctx["image"] = image_data
        print(ctx)
        return ctx
