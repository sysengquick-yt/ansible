# (c) 2024 John Ratliff <john@technoplaza.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)  # noqa: E501

from __future__ import annotations

import re

from ansible.errors import AnsibleFilterError


def qcow2_image_name(filename: str) -> str:
    if not filename.endswith(".qcow2"):
        filename += ".qcow2"

    return filename


def checksum(checksum_file: str, filename: str) -> str:
    try:
        with open(checksum_file, "r") as f:
            for line in f:
                if match := re.match(
                    r"SHA(256|512) \(" + filename + r"\) = ([a-f0-9]+)", line
                ):
                    return f"sha{match.group(1)}:{match.group(2)}"
                if match := re.match(r"([0-9a-f]+) [ *]" + filename, line):
                    checksum = match.group(1)
                    length = len(checksum)

                    if length == 64:
                        return f"sha256:{checksum}"
                    elif length == 128:
                        return f"sha512:{checksum}"
                    else:
                        raise AnsibleFilterError(
                            f"Unexpected checksumn length {length}. Expected 64 or 128."
                        )
    except IOError as e:
        raise AnsibleFilterError(
            f"Unable to read checksum data from {checksum_file}", orig_exc=e
        )

    raise AnsibleFilterError(
        f"Unable to find checksum for {filename} in {checksum_file}"
    )


class FilterModule(object):
    def filters(self):
        return {
            "checksum": checksum,
            "qcow2_image_name": qcow2_image_name,
        }
