from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from resourcemanager.resourcespace.browser.search import ResourceSpaceSearch


class ResourceSearch(BrowserView):
    """Search selected resources
    """

    template = ViewPageTemplateFile('templates/rm_search.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.search_context = 'rm-search'
        self.resources = [ResourceSpaceSearch(context, request)]

    def __call__(self):
        self.search_context = self.request._steps[-1]
        return self.template()


class ResourceCopy(BrowserView):
    """Copy selected media to the current folder
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
