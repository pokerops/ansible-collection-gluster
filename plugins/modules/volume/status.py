from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.volume import status_detail

DOCUMENTATION = """
    module: status
    short_description: Custom plugin to get volume status
    description: Custom plugin to get volume status
    options:
        volname:
            description: Volume name
            required: false
            type: str
        group_subvols:
            description: Subolumes
            required: false
            type: str
"""

def run_module():

    module_args = {
        "volname": {"default": None, "type": "str"},
        "group_subvols": {"default": None, "type": "str"}
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
            changed=False,
            msg="Command executed successfully",
            results=status_detail(**params)
        )
        module.exit_json(**result)

    except FileNotFoundError as e:
        if 'gluster' in str(e):
            module.fail_json(
                changed=False,
                msg="",
                stderr="GlusterFS CLI not found: is Gluster installed?",
                result=[]
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

    
    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}", changed=False)

def main():
    run_module()

if __name__ == '__main__':
    main()
