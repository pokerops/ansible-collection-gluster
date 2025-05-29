from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.georep import status

def run_module():

    module_args = {
        "primary_volume": {"default": None, "type": "str"},
        "secondary_host": {"default": None, "type": "str"},
        "secondary_volume": {"default": None, "type": "str"},
        "secondary_user": {"required": True, "type": "str"}
    }

    result = dict(
        changed=False,
        msg='',
        results=[],
    )

    params = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        result['msg'] = "Command executed successfully"
        result['results'] = status(**params)
        module.exit_json(**result)

    except GlusterCmdException as e:
        rc, out, err = e.args[0]

        out = out.strip() if out else ""
        err = err.strip() if err else ""

        if rc == 2 and (
            "geo-replication command failed" in out.lower() or
            "geo-replication command failed" in err.lower()
        ):
            module.exit_json(
                changed=False,
                msg="No geo-replication sessions exist",
                result=[],
                debug={
                    "rc": rc,
                    "stdout": out.strip(),
                    "stderr": err.strip() if err else ""
                }
            )

        module.fail_json(
            msg="Gluster command failed unexpectedly",
            rc=rc,
            stdout=out,
            stderr=err,
            changed=False
        )

def main():
    run_module()

if __name__ == '__main__':
    main()
