from ansible.module_utils.common.validation import safe_eval
from ansible.module_utils.basic import AnsibleModule
from glustercli.cli.georep import create

def run_module():

    module_args = {
        "volume": {"required": True, "type": "str"},
        "slave": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "push_pem": {"default": True, "type": "bool"},
        "no_verify": {"default": False, "type": "bool"},
        "ssh_port": {"default": "22", "type": "str"},
        "force": {"default": False, "type": "bool"}
    }

    module = AnsibleModule(argument_spec=module_args)

    primary_volume = module.params["volume"]

    secondary_volume = module.params["volume"]

    secondary_host = module.params["slave"]

    secondary_user = module.params["user"]

    push_pem = module.params["push_pem"]

    no_verify = module.params["no_verify"]

    ssh_port = module.params["ssh_port"]

    force = module.params["force"]

    try:
        georep_create = create(primary_volume, secondary_host, secondary_volume, secondary_user,
                               push_pem, no_verify, force, ssh_port)

    except:

        georep_create = ""

    module.exit_json(changed=False, result=georep_create)

def main():
    run_module()

if __name__ == '__main__':
    main()
