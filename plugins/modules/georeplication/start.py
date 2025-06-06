from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.georep import start

DOCUMENTATION = """
    module: start
    short_description: Custom plugin to start gluster geo replication sessions
    description: Custom plugin to start gluster geo replication sessions
    options:
        primary_volume:
            description: Name of the primary volume
            required: false
            type: str
        secondary_volume:
            description: Name of the secondary volume
            required: false
            type: str
        secondary_host:
            description: Name of the secondary host
            required: false
            type: str
        secondary_user:
            description: Name of the secondary user
            required: true
            type: str
        force:
            description: Force gluster geo replication session start
            required: false
            type: bool
"""

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
            result=start(**params)
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
