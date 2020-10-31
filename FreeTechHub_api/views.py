from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import datetime
import os

class UploadImgView(APIView):
    
    def post(self, request, format=None):

        img = request.FILES.get("image")
        extension = img.name.rsplit(".")[1]

        # form the image name
        img_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                   '.' + extension

        # write the actual image into disk
        img_path = os.path.join(settings.IMG_DIR, img_name)
        destination = open(img_path, 'wb+')
        for chunk in img.chunks():
            destination.write(chunk)
        destination.close()

        return Response(settings.IMG_URL+img_name)