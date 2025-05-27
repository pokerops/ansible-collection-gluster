from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from glustercli.cli.georep import status

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, user=None):

        return ([status(secondary_user=user)])
