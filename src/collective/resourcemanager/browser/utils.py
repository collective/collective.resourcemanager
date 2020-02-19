import requests
from PIL import Image
from plone.namedfile.file import NamedBlobImage
from zope.schema import ValidationError


def set_url_as_image(url, image_field, value):
    """For NamedRSImageWidget, set a url as the image
    """
    if url:
        response = requests.get(url)
        try:
            Image.open(requests.get(url, stream=True).raw)
        except OSError as e:
            raise ValidationError(
                '{}\n Resource url may be invalid'.format(e))
        blob = NamedBlobImage(
            data=response.content)
        curr_img = image_field
        if not curr_img:
            image_field = blob
            return blob
        elif image_field.getFirstBytes() != blob.getFirstBytes():
            image_field = blob
            return blob
    else:
        image_field = value
        return value
    return None
