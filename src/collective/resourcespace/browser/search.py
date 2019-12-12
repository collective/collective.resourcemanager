import hashlib
import json
import requests
import urllib.parse
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
        user_query = 'user={0}'.format(self.rs_user) + query
        key_query = self.rs_private_key + user_query
        hash.update(key_query.encode('utf-8'))
        request_url = self.rs_url + '?' + user_query + '&sign=' + hash.hexdigest()
        exc = requests.exceptions
        try:
            response = requests.get(request_url, timeout=5)
        except (exc.ConnectTimeout, exc.ConnectionError) as e:
            self.messages.append(str(e))
            return []
        if response.status_code != 200:
            self.messages.append(response.reason)
            return []
        try:
            return response.json()
        except ValueError:
            self.messages.append('The json returned from {0} is not valid'.format(
                user_query
            ))
            return []

    def __call__(self):
        form = self.request.form
        search_term = form.get('rs_search')
        browse_term = form.get('rs_browse')
        if not form or not(search_term or browse_term):
            return self.template()
        # do the search based on term or collection name
        if search_term:
            search_term = urllib.parse.quote_plus(form['rs_search'])
        else:
            search_term = urllib.parse.quote_plus('!' + browse_term)
        query = '&function=do_search&param1={0}&param2=1'.format(
            search_term
        )
        response = self.query_resourcespace(query)
        self.image_metadata = {x['ref']: x for x in response}
        self.num_results = len(response)
        media_ids = [x['ref'] for x in response[:100]]
        # build new query to return image urls
        query2 = '&function=get_resource_path&param1=%5B{0}%5D&param2=false&param3=scr'.format(
            ','.join(media_ids)
        )
        self.image_urls = self.query_resourcespace(query2)
        if not self.image_urls and not self.messages:
            self.messages.append("No images found")
        if form.get('type', '') == 'json':
            return json.dumps({
                'errors': self.messages,
                'metadata': self.image_metadata,
                'urls': self.image_urls,
                })
        return self.template()

    def collections(self):
        query = '&function=search_public_collections&param2=name&param3=ASC&param4=0'
        response = self.query_resourcespace(query)
        return response
