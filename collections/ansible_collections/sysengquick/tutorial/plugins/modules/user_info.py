#!/usr/bin/python

# Copyright: (c) 2024, John Ratliff <john@techoplaza.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)  # noqa: E501
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pwd

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = {
        "username": {
            "type": "str",
            "required": True,
        }
    }

    result = {
        "changed": False,
        "failed": True,
        "message": "Failed to fetch user information",
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        user_info = pwd.getpwnam(module.params["username"])
    except KeyError:
        module.exit_json(**result)

    result["failed"] = False
    result["message"] = "Successfully fetched user information"
    result["user_info"] = {
        "username": user_info.pw_name,
        "uid": user_info.pw_uid,
        "gid": user_info.pw_gid,
        "home": user_info.pw_dir,
    }

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
