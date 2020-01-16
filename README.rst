==========================
collective.resourcemanager
==========================

Features
--------

collective.resourcemanager is a base package, meant to be used with resourcemanager.* add-ons.
Currently, only resourcemanager.resourcespace is available for connecting to ResourceSpace.

Provides base functionality for searching a digital asset manager to then use selected images within Plone.

There are two main ways to do this:
* On folderish types, you can search a DAM for images to copy into that folder
* On a page (for example), a replacement lead image behavior will allow you to use
  an image from the DAM as the lead image. Image is copied into Plone.

This add-on will always copy the images into Plone, so they are hosted on the same platform and server.


Installation
------------

Install collective.resourcemanager and any resourcemanager.* packages by adding them to your buildout::

    [instance]
    ...
    eggs =
        ...
        collective.resourcemanager
        resourcemanager.resourcespace


Run ``bin/buildout``, and start the instance.

Within Plone:

* Install the add-ons in the Add-ons Control Panel
* For content types that will use the custom lead image behavior:
  * Go to the Dexterity Content Types Control Panel
  * Select the desired content type (like Page)
  * Click on the Behaviors tab
  * Select the box for 'ResourceManager Image field'
  * Make sure 'Lead Image' is not selected
  * Save
* See README for resourcemanager.* packages for more information


Use
---

Folders
=======
* On a folderish content type, click 'Import from DAM' on the edit bar
* Browse or search for images
* Click 'Use this image' to copy the image from the external resource into the current Plone Folder

Lead Image
==========
When the 'ResourceManager Image field' behavior is enabled for your content types,
you will be able to search the DAM for images to be used as the lead image.

* Add/Edit a piece of content where the behavior is enabled
* You will see an 'Image' field that is similar to the lead image
* Click 'Browse Resources' to search the DAM, and click 'Use this image'
* The image url will display in the field
* When the page is saved, the image is copied from the URL and used as the lead image
  * Note the url is used to copy the image into the Plone site, the page will not point to the external site


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.resourcemanager/issues
- Source Code: https://github.com/collective/collective.resourcemanager


License
-------

The project is licensed under the GPLv2.
