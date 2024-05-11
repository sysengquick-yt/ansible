# (c) 2024 John Ratliff <john@technoplaza.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)  # noqa: E501
from __future__ import annotations

import pathlib
from typing import Dict, TypeAlias

import yaml
from pydantic import BaseModel, HttpUrl, ValidationError

from ansible.errors import AnsibleError, AnsibleLookupError
from ansible.plugins.lookup import LookupBase


class CloudImagePropertiesModel(BaseModel):
    url: HttpUrl
    checksum: str
    image: str


CloudImages: TypeAlias = Dict[str, CloudImagePropertiesModel]


class CloudImagesModel(BaseModel):
    cloud_images: CloudImages


class LookupModule(LookupBase):
    cloud_images: CloudImages = None

    @classmethod
    def _load_cloud_images(cls):
        if cls.cloud_images is None:
            filename = (
                pathlib.Path(__file__).parent.resolve() / "data" / "cloud_images.yaml"
            )

            try:
                with open(filename, "r") as f:
                    data = yaml.safe_load(f)
            except IOError:
                raise AnsibleError(
                    f"Unable to load cloud image files data from {filename}"
                )
            except yaml.YAMLError:
                raise AnsibleError(f"Unable to parse yaml from {filename}")

            try:
                cls.cloud_images = CloudImagesModel(**data).cloud_images
            except ValidationError as e:
                raise AnsibleError(
                    f"Unable to validate cloud image file data in {filename}",
                    orig_exc=e,
                )

    def run(self, terms, variables=None, **kwargs):
        self._load_cloud_images()

        terms_count = len(terms)

        if terms_count != 1:
            raise AnsibleLookupError(
                f"Expected exactly 1 image name; received {terms_count}"
            )

        image_name = terms[0]

        if image_name not in self.cloud_images:
            raise AnsibleLookupError(f"Unable to find image {image_name}")

        image_properties = self.cloud_images[image_name]

        filename = image_properties.image

        if not filename.endswith(".qcow2"):
            filename += ".qcow2"

        image = {
            "checksum_url": f"{image_properties.url}/{image_properties.checksum}",
            "image_url": f"{image_properties.url}/{image_properties.image}",
            "filename": filename,
        }

        return [image]
