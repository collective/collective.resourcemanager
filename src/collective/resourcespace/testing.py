# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.resourcespace


class CollectiveResourcespaceLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.resourcespace)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.resourcespace:default')


COLLECTIVE_RESOURCESPACE_FIXTURE = CollectiveResourcespaceLayer()


COLLECTIVE_RESOURCESPACE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_RESOURCESPACE_FIXTURE,),
    name='CollectiveResourcespaceLayer:IntegrationTesting',
)


COLLECTIVE_RESOURCESPACE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_RESOURCESPACE_FIXTURE,),
    name='CollectiveResourcespaceLayer:FunctionalTesting',
)


COLLECTIVE_RESOURCESPACE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_RESOURCESPACE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveResourcespaceLayer:AcceptanceTesting',
)
