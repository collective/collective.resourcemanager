import hashlib
import requests
import urllib.parse
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
        self.messages = []

    def query_resourcespace(self, query):
        hash = hashlib.sha256()
        key_query = self.rs_private_key + query
        hash.update(key_query.encode('utf-8'))
        request_url = self.rs_url + '?' + query + '&sign=' + hash.hexdigest()
        response = requests.get(request_url)
        if response.status_code != 200:
            self.messages.append(response.reason)
            return []
        return response.json()

    def __call__(self):
        form = self.request.form
        search_term = form.get('rs-search')
        browse_term = form.get('rs-browse')
        if not form or not(search_term or browse_term):
            return self.template()
        # do the search based on term or collection name
        if search_term:
            search_term = urllib.parse.quote_plus(form['rs-search'])
        else:
            search_term = urllib.parse.quote_plus('!' + browse_term)
        query = 'user={0}&function=do_search&param1={1}&param2=1'.format(
            self.rs_user, search_term
        )
        response = self.query_resourcespace(query)
        self.image_metadata = {x['ref']: x for x in response}
        self.num_results = len(response)
        media_ids = [x['ref'] for x in response[:100]]
        # build new query to return image urls
        query2 = 'user={0}&function=get_resource_path&param1=%5B{1}%5D&param2=false&param3=scr'.format(
            self.rs_user, ','.join(media_ids)
        )
        self.image_urls = self.query_resourcespace(query2)
        if not self.image_urls and not self.messages:
            self.messages.append("No images found")
        return self.template()

    def collections(self):
        query = 'user={0}&function=search_public_collections&param2=name&param3=ASC&param4=0'.format(
            self.rs_user
        )
        response = self.query_resourcespace(query)
        return response
