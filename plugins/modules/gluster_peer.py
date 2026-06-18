import re
import socket

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import safe_eval
from glustercli.cli.peer import detach_all, pool, probe
from glustercli.cli.utils import GlusterCmdException

DOCUMENTATION = """
    module: gluster_peer
    short_description: Custom plugin to manage pool members
    description: Custom plugin to manage pool members
    options:
        nodes:
            description: List of gluster members
            required: true
            type: list
        state:
            description: State for gluster node
            required: false
            type: bool
"""


def manage_nodes(**params):
    result = {}
    result["msg"] = ""
    result["changed"] = False
    nodes = params["nodes"]
    action = params["action"]
    msg = ""

    if len(nodes) == 0:
        result["msg"] = "There are no new nodes to add"
        return result

    for node in nodes:
        if action == "probe":
            output = probe(node)
            msg = "Nodes were added successfully"
        else:
            output = detach_all()
            msg = "Nodes were removed successfully"

        if "already in peer" in output or "localhost not needed" in output:
            result["changed"] = False
        else:
            result["changed"] = True
    result["msg"] = msg
    return result


def run_module():
    module_args = {
        "nodes": {"required": True, "type": "list"},
        "state": {
            "default": "present",
            "type": "str",
            "choices": ["absent", "present"],
        },
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    params = {}

    for key, value in module_args.items():
        params[key] = module.params[key]

    if not params["nodes"]:
        module.fail_json(msg=f"Nodes list cannot be empty", changed=False)

    if params["state"] == "present":
        results = pool()
        members = [member["hostname"] for member in results]
        hostname = socket.gethostname()
        existing = list(map(lambda h: re.sub(r"localhost", hostname, h), members))
        params["nodes"] = [host for host in params["nodes"] if host not in existing]
        params["action"] = "probe"
    else:
        params["action"] = "detach"

    try:
        result = manage_nodes(**params)
        module.exit_json(**result)

    except FileNotFoundError as e:
        if "gluster" in str(e):
            module.fail_json(
                changed=False,
                msg="",
                stderr="GlusterFS CLI not found: is Gluster installed?",
                results=[],
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
            changed=False,
        )

    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}", changed=False)


def main():
    run_module()


if __name__ == "__main__":
    main()
