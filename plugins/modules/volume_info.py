from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.volume import info

def run_module():
    module_args = {
        "volname": {"default": None, "type": "str"}
    }

    params = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    result = dict(
        changed=False,
        msg='',
        results=[],
    )

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        result['msg'] = "Command executed successfully"
        result['results'] = info(**params)
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
