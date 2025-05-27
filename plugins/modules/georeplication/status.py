from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.georep import status

def run_module():

    module_args = {
        "volume": {"default": None, "type": "str"},
        "slave": {"default": None, "type": "str"},
        "user": {"required": True, "type": "str"}
    }

    module = AnsibleModule(argument_spec=module_args)

    primary_volume = module.params["volume"]

    secondary_volume = module.params["volume"]

    secondary_host = module.params["slave"]

    secondary_user = module.params["user"]

    try:
        georep = status(primary_volume, secondary_host, secondary_volume, secondary_user)

    except:

        georep = []

    if len(georep) > 0:
        georep_status = georep[0]

    else:
        georep_status = []

    module.exit_json(changed=False, result=georep_status)

def main():
    run_module()

if __name__ == '__main__':
    main()
