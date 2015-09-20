import io

from PIL import Image

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Photo


def thumbnail(request, pk):

    photo = get_object_or_404(Photo, pk=pk)

    img = Image.open(photo.src.path)

    # We're gonna scale to 300px high...
    height = 300
    width = int(round(img.size[0] * height / float(img.size[1])))

    img = img.resize((width, height), Image.ANTIALIAS)

    tmp = io.BytesIO()
    img.save(tmp, format='JPEG', quality=85)

    return HttpResponse(tmp.getvalue(), content_type='image/jpeg')
