# -*- coding: utf-8 -*-
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer, Interface

from collective.resourcemanager.browser.widget import NamedRSImageWidget
from .utils import set_url_as_image


class IBrowseRS(Interface):
    pass


@provider(IFormFieldProvider)
class IBrowseRSBehavior(model.Schema):

    image = namedfile.NamedBlobImage(
        title=u"Image",
        description=u"Upload image or browse resources",
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
        if value:
            self.context.image = value
        else:
            req = self.context.REQUEST
            url = 'rs-url-input' in req and req['rs-url-input']
            if not url:
                self.context.image = value
            blob = set_url_as_image(url, self.context.image, value)
            self.context.image = blob

    @property
    def image_caption(self):
        return self.context.image_caption

    @image_caption.setter
    def image_caption(self, value):
        self.context.image_caption = value


@provider(IFormFieldProvider)
class IImageResourceData(model.Schema):

    external_img_id = schema.TextLine(
        title=u"External Resource ID",
        description=u"",
        required=False,
        readonly=False,
    )
    resource_metadata = schema.Text(
        title=u"Resource Metadata",
        description=u"Additional information from the external resource",
        required=False,
    )
