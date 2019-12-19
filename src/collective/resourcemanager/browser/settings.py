from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from zope.interface import Interface
# from zope import schema


class IResourceSettings(Interface):
    """Resource Manager Settings
    """


class ResourceSettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IResourceSettings
    label = u"ResourceManager Settings"


class ResourceKeysView(ControlPanelFormWrapper):
    form = ResourceSettingsEditForm
