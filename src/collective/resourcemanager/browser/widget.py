# -*- coding: utf-8 -*-
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import NamedImageWidget
# from z3c.form.interfaces import IFieldWidget
# from z3c.form.widget import FieldWidget
from zope import schema
from zope.interface import implementer


class INamedRSImageWidget(INamedFileWidget):
    """A widget for a named image field
    """

    width = schema.Int(title=u"Image width", min=0, required=False)
    height = schema.Int(title=u"Image height", min=0, required=False)
    thumb_tag = schema.Text(title=u"Thumbnail image tag", required=False)
    alt = schema.TextLine(title=u"Image alternative text", required=False)


@implementer(INamedRSImageWidget)
class NamedRSImageWidget(NamedImageWidget):
    klass = u'named-rsimage-widget'
