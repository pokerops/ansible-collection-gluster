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

    primary_volume secondary_volume = module_args["volume"]

    secondary_host = module_args["slave"]

    secondary_user = module_args["user"]

    georep_status = status(primary_volume, secondary_host, 
                           secondary_volume, secondary_user)

    result = {
        "status": georep_status
    }

    module.exit_json(changed=False, meta=result)

def main():
    run_module()

if __name__ == '__main__':
    main()
