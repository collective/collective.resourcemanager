# -*- coding: utf-8 -*-
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as namedfile
from plone.supermodel import model
from zope.interface import alsoProvides

from collective.resourcespace.browser.widget import NamedRSImageWidget


class IBrowseRS(model.Schema):

    image = namedfile.NamedBlobImage(
        title=u"Image",
        description=u"Upload image or browse ResourceSpace",
        required=False,
    )
    directives.widget(
        'image',
        NamedRSImageWidget)


alsoProvides(IBrowseRS, IFormFieldProvider)
