# -*- coding: utf-8 -*-
import requests
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.namedfile.file import NamedBlobImage
from plone.supermodel import model
from zope.component import adapter
from zope.interface import provider, implementer

from collective.resourcespace.browser.widget import NamedRSImageWidget


@provider(IFormFieldProvider)
class IBrowseRS(model.Schema):

    image = namedfile.NamedBlobImage(
        title=u"Image",
        description=u"Upload image or browse ResourceSpace",
        required=False,
    )
    directives.widget(
        'image',
        NamedRSImageWidget)


@implementer(IBrowseRS)
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
            # TODO: handle errors on url
            blob = NamedBlobImage(
                data=response.content)
            curr_img = self.context.image
            if not curr_img:
                self.context.image = blob
            elif self.context.image.getFirstBytes() != blob.getFirstBytes():
                self.context.image = blob
        else:
            self.context.image = value
