from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.volume import optreset

def run_module():
    module_args = {
        "volname": {"default": None, "type": "str"},
        "opt": {"default": None, "type": "str"},
        "force": {"default": None, "type": "bool"}
    }

    params = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    for key, value in module_args.items():
        params[key] = module.params[key]

    try:
        result = dict(
            changed=True,
            msg="Command executed successfully",
            result=optreset(**params)
        )
        module.exit_json(**result)

    except FileNotFoundError as e:
        if 'gluster' in str(e):
            module.fail_json(
                changed=False,
                msg="",
                stderr="GlusterFS CLI not found: is Gluster installed?",
                result=""
            )
        else:
            module.fail_json(msg=f"File not found: {str(e)}", changed=False)

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
