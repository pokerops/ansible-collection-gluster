from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.utils import GlusterCmdException
from glustercli.cli.gluster_version import glusterfs_version

def run_module():
    module_args = {}

    module = AnsibleModule(
        argument_spec=module_args
    )

    result = dict(
        changed=False,
        msg='',
        result="",
    )

    try:
        result['msg'] = "Command executed successfully"
        result['result'] = glusterfs_version().split(' ')[1]
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
