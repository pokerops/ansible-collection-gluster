from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.georep import stop

def run_module():

    module_args = {
        "primary_volume": {"default": None, "type": "str"},
        "secondary_host": {"default": None, "type": "str"},
        "secondary_volume": {"default": None, "type": "str"},
        "secondary_user": {"required": True, "type": "str"},
        "force": {"default": False, "type": "bool"}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    params = {}

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        result = dict(
            changed=True,
            msg="Command executed successfully",
            result=stop(**params)
        )
        module.exit_json(**result)

    except GlusterCmdException as e:
        rc, out, err = e.args[0]
        module.fail_json(
            msg=f"Gluster command failed: {err.strip()}",
            rc=rc,
            stdout=out,
            stderr=err,
            changed=False
        )

def main():
    run_module()

if __name__ == '__main__':
    main()
