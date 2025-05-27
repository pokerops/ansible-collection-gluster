from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from glustercli.cli.georep import status

display = Display()

class LookupModule(LookupBase):
    def run(self, primary_volume=None, secondary_host=None,
            secondary_volume=None, secondary_user="root")

        return ([status(primary_volume=primary_volume, secondary_host=secondary_host,
                secondary_volume=secondary_volume, secondary_user=secondary_user)])
