from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from glustercli.cli.georep import status

display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        return ([status(primary_volume=primary_volume, secondary_host=secondary_host,
                secondary_volume=secondary_volume, secondary_user=user)])
