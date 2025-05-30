from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.georep import status

def session_is_healthy(session_entries):
    return all(
        entry.get("status", "").strip().lower() in ("active", "passive")
        for entry in session_entries
    )

def run_module():

    module_args = {
        "primary_volume": {"default": None, "type": "str"},
        "secondary_host": {"default": None, "type": "str"},
        "secondary_volume": {"default": None, "type": "str"},
        "secondary_user": {"required": True, "type": "str"}
    }

    params = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        georep_status = status(**params)
        flattened_status = [session for sessions in georep_status for session in sessions]
        result = dict(
            changed=True,
            msg="Command executed successfully",
            results=flattened_status
        )

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
                results=[],
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
