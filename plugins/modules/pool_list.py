from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.peer import pool

def run_module():
    module_args = {}

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    try:
        result = dict(
            changed=False,
            msg="Command executed successfully",
            results=pool()
        )
        module.exit_json(**result)

    except FileNotFoundError as e:
        if 'gluster' in str(e):
            module.fail_json(
                changed=False,
                msg="",
                stderr="GlusterFS CLI not found: is Gluster installed?",
                results=[]
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
