from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import georep_execute

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

    cmd = [primary_volume,
           f"{secondary_user}@{secondary_host}::{secondary_volume}",
           "delete"]

    if reset_sync_time is not None:
        cmd += ["reset-sync-time"]

    try:
        georep_delete = georep_execute(cmd)

    except:

        georep_delete = ""

    module.exit_json(changed=False, result=georep_delete)

def main():
    run_module()

if __name__ == '__main__':
    main()
