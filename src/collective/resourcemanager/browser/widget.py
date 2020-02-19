# -*- coding: utf-8 -*-
from plone.dexterity.browser import add
from plone.dexterity.browser.edit import DefaultEditForm
from plone.formwidget.namedfile.interfaces import INamedFileWidget
from plone.formwidget.namedfile.validator import InvalidState
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.namedfile.interfaces import INamedImageField
from z3c.form import validator
from zope import schema
from zope.interface import implementer

from .utils import set_url_as_image


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


class CustomImageValidator(validator.SimpleFieldValidator):
    """For NamedRSImageWidget, validation should pass
       if there is a resource url
    """

    def validate(self, value, force=False):
        if 'NamedRSImageWidget' not in str(self.widget.__class__):
            # run original validation for default widget
            action = self.request.get("%s.action" % self.widget.name, None)
            if action == 'replace' and value is None:
                raise InvalidState()
            return super(CustomImageValidator, self).validate(value, force)

        # if field is not required, we don't need to validate
        if not self.widget.required:
            return
        resource_url = self.request.get('rs-url-input')
        if not resource_url:
            # raise Invalid("Missing Input")
            raise InvalidState()


validator.WidgetValidatorDiscriminators(
    CustomImageValidator,
    field=INamedImageField,
    )


def handle_resource_image(obj, event):
    """If an external resource was selected,
       copy it into the field, and set resource data
    """
    resource_url = obj.REQUEST.get('rs-url-input')
    blob = set_url_as_image(resource_url, obj.image, None)
    obj.image = blob
    # TODO: apply resource_metadata, title, description
    obj.reindexObject()
