from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import georep_execute

def run_module():

    module_args = {
        "volume": {"required": True, "type": "str"},
        "slave": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "key": {"required": True, "type": "str"},
        "value": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=module_args)

    primary_volume = module.params["volume"]

    secondary_volume = module.params["volume"]

    secondary_host = module.params["slave"]

    secondary_user = module.params["user"]

    key = module.params["key"]

    value = module.params["value"]

    cmd = [primary_volume,
           f"{secondary_user}@{secondary_host}::{secondary_volume}",
           "config", key, value]

    try:
        georep_config_set = georep_execute(cmd)

    except:

        georep_config_set = ""

    module.exit_json(changed=False, result=georep_config_set)

def main():
    run_module()

if __name__ == '__main__':
    main()
