# -*- coding: utf-8 -*-
from plone.dexterity.browser import add
from plone.dexterity.browser.edit import DefaultEditForm
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.widget import NamedImageWidget
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


class ImageAddForm(add.DefaultAddForm):

    def updateWidgets(self, prefix=None):
        super(ImageAddForm, self).updateWidgets()
        image = self.widgets['image']
        image.__class__ = NamedRSImageWidget
        self.widgets.update()


class ImageAddView(add.DefaultAddView):
    form = ImageAddForm


class ImageEdit(DefaultEditForm):

    def updateWidgets(self, prefix=None):
        super(ImageEdit, self).updateWidgets()
        image = self.widgets['image']
        image.__class__ = NamedRSImageWidget
        self.widgets.update()
