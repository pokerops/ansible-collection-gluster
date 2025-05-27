from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.georep import start

def run_module():

    module_args = {
        "volume": {"required": True, "type": "str"},
        "slave": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "force": {"default": False, "type": "bool"}
    }

    module = AnsibleModule(argument_spec=module_args)

    primary_volume = module.params["volume"]

    secondary_volume = module.params["volume"]

    secondary_host = module.params["slave"]

    secondary_user = module.params["user"]

    force = module.params["force"]

    try:
        georep_start = start(primary_volume, secondary_host, secondary_volume, secondary_user, force)

    except:

        georep_start = ""

    module.exit_json(changed=False, result=georep_start)

def main():
    run_module()

if __name__ == '__main__':
    main()
