from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import georep_execute, GlusterCmdException

DOCUMENTATION = """
    module: delete
    short_description: Custom plugin to delete gluster geo replication sessions
    description: Custom plugin to delete gluster geo replication sessions
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
        reset_sync_time:
            description: Reset sync time for session
            required: false
            type: bool
"""

def run_module():

    module_args = {
        "primary_volume": {"default": None, "type": "str"},
        "secondary_host": {"default": None, "type": "str"},
        "secondary_volume": {"default": None, "type": "str"},
        "secondary_user": {"required": True, "type": "str"},
        "reset_sync_time": {"default": False, "type": "bool"}
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    params = {}

    params = module.params

    try:
        secondary_target = f"{params['secondary_user']}@{params['secondary_host']}::{params['secondary_volume']}"
        cmd = [
            params['primary_volume'],
            secondary_target,
            "delete"
        ]

        if params['reset_sync_time'] is not None:
            cmd += ["reset-sync-time"]

        result = dict(
            changed=True,
            msg="Command executed successfully",
            result=georep_execute(cmd)
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
            result="",
            changed=False
        )

def main():
    run_module()

if __name__ == '__main__':
    main()
