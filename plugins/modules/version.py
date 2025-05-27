from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.gluster_version import glusterfs_version

def run_module():
    module_args = {}

    module = AnsibleModule(
        argument_spec=module_args
    )

    version = glusterfs_version().split(' ')[0]

    result = {
        "version": version
    }

    module.exit_json(changed=False, meta=result)

def main():
    run_module()

if __name__ == '__main__':
    main()
