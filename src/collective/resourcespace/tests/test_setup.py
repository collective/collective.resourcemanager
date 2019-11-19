# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.resourcespace.testing import COLLECTIVE_RESOURCESPACE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.resourcespace is properly installed."""

    layer = COLLECTIVE_RESOURCESPACE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.resourcespace is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.resourcespace'))

    def test_browserlayer(self):
        """Test that ICollectiveResourcespaceLayer is registered."""
        from collective.resourcespace.interfaces import (
            ICollectiveResourcespaceLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveResourcespaceLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_RESOURCESPACE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.resourcespace'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.resourcespace is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.resourcespace'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveResourcespaceLayer is removed."""
        from collective.resourcespace.interfaces import \
            ICollectiveResourcespaceLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveResourcespaceLayer,
            utils.registered_layers())
