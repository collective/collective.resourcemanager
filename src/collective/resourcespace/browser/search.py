import hashlib
import requests
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ResourceSpaceSearch(BrowserView):
    """Search ResourceSpace Media
       Copy selected media to the current folder
    """

    template = ViewPageTemplateFile('templates/rs_search.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        reg_prefix = 'collective.resourcespace.browser.settings.IResourceSpaceKeys'
        self.rs_url = context.portal_registry['{0}.rs_url'.format(reg_prefix)]
        self.rs_user = context.portal_registry['{0}.rs_user'.format(reg_prefix)]
        self.rs_private_key = context.portal_registry['{0}.rs_private_key'.format(reg_prefix)]
        self.image_urls = []

    def query_resourcespace(self, query):
        hash = hashlib.sha256()
        hash.update(self.rs_private_key + query)
        request_url = self.rs_url + '?' + query + '&sign=' + hash.hexdigest()
        response = requests.get(request_url)
        # TODO: handle various errors from the response here
        return response.json()
    
    def __call__(self):
        form = self.request.form
        if not form or 'rs-search' not in form:
            return self.template()
        # do the search
        search_term = form['rs-search']
        query = 'user={0}&function=do_search&param1={1}'.format(
            self.rs_user, search_term
        )
        response = self.query_resourcespace(query)
        media_ids = [x['ref'] for x in response]
        # build new query to return image urls
        query2 = 'user={0}&function=get_resource_path&param1=[{1}]&param2=false'.format(
            self.rs_user, ','.join(media_ids)
        )
        self.image_urls = self.query_resourcespace(query2)
        return self.template()
