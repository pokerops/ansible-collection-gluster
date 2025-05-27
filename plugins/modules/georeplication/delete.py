from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.georep import delete

def run_module():

    module_args = {
        "volume": {"required": True, "type": "str"},
        "slave": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "reset_sync_time": {"default": False, "type": "bool"}
    }

    module = AnsibleModule(argument_spec=module_args)

    primary_volume = module.params["volume"]

    secondary_volume = module.params["volume"]

    secondary_host = module.params["slave"]

    secondary_user = module.params["user"]

    reset_sync_time = module.params["reset_sync_time"]

    try:
        georep_delete = delete(primary_volume, secondary_host, secondary_volume, secondary_user, reset_sync_time)

    except:

        georep_delete = ""

    module.exit_json(changed=False, result=georep_delete)

def main():
    run_module()

if __name__ == '__main__':
    main()
