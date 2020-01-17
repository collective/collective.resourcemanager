# -*- coding: utf-8 -*-
import requests
from PIL import Image
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.namedfile.file import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer, Interface
from zope.schema import ValidationError

from collective.resourcemanager.browser.widget import NamedRSImageWidget


class IBrowseRS(Interface):
    pass


@provider(IFormFieldProvider)
class IBrowseRSBehavior(model.Schema):

    image = namedfile.NamedBlobImage(
        title=u"Image",
        description=u"Upload image or browse ResourceSpace",
        required=False,
    )
    directives.widget(
        'image',
        NamedRSImageWidget)

    image_caption = schema.TextLine(
        title=u'Image Caption',
        description=u'',
        required=False,
    )


@implementer(IBrowseRSBehavior)
@adapter(IDexterityContent)
class BrowseRS(object):
    """If URL was entered, store to NamedBlobImage
    """

    def __init__(self, context):
        self.context = context

    @property
    def image(self):
        return self.context.image

    @image.setter
    def image(self, value):
        req = self.context.REQUEST
        url = 'rs-url-input' in req and req['rs-url-input']
        if url:
            response = requests.get(url)
            try:
                Image.open(requests.get(url, stream=True).raw)
            except OSError as e:
                raise ValidationError(
                    '{}\n ResourceSpace url may be invalid'.format(e))
            blob = NamedBlobImage(
                data=response.content)
            curr_img = self.context.image
            if not curr_img:
                self.context.image = blob
            elif self.context.image.getFirstBytes() != blob.getFirstBytes():
                self.context.image = blob
        else:
            self.context.image = value

    @property
    def image_caption(self):
        return self.context.image_caption

    @image_caption.setter
    def image_caption(self, value):
        self.context.image_caption = value


@provider(IFormFieldProvider)
class IImageResourceData(model.Schema):

    external_url = schema.TextLine(
        title=u"External Resource URL",
        description=u"",
        required=False,
    )
