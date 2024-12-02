#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""AWS Code Build image builder flavor."""

from typing import TYPE_CHECKING, Optional, Type

from zenml.image_builders import BaseImageBuilderConfig, BaseImageBuilderFlavor
from zenml.integrations.aws import (
    AWS_CONNECTOR_TYPE,
    AWS_IMAGE_BUILDER_FLAVOR,
    AWS_RESOURCE_TYPE,
)
from zenml.models import ServiceConnectorRequirements

if TYPE_CHECKING:
    from zenml.integrations.aws.image_builders import AWSImageBuilder


class AWSImageBuilderConfig(BaseImageBuilderConfig):
    """AWS Code Build image builder configuration.

    Attributes:
        code_build_project: The name of the AWS CodeBuild project to use to
            build the image.
        region: The AWS region where the processing job will be run. If not
            provided, the value from the default AWS config will be used.
        implicit_container_registry_auth: Whether to use implicit authentication
            to authenticate the AWS Code Build build to the container registry
            when pushing container images. If set to False, the container
            registry credentials must be explicitly configured for the container
            registry stack component or the container registry stack component
            must be linked to a service connector.
            NOTE: When implicit_container_registry_auth is set to False, the
            container registry credentials will be passed to the AWS Code Build
            build as environment variables. This is not recommended for
            production use unless your service connector is configured to
            generate short-lived credentials.
    """

    code_build_project: str
    region: Optional[str] = None
    implicit_container_registry_auth: bool = True


class AWSImageBuilderFlavor(BaseImageBuilderFlavor):
    """AWS Code Build image builder flavor."""

    @property
    def name(self) -> str:
        """The flavor name.

        Returns:
            The name of the flavor.
        """
        return AWS_IMAGE_BUILDER_FLAVOR

    @property
    def service_connector_requirements(
        self,
    ) -> Optional[ServiceConnectorRequirements]:
        """Service connector resource requirements for service connectors.

        Specifies resource requirements that are used to filter the available
        service connector types that are compatible with this flavor.

        Returns:
            Requirements for compatible service connectors, if a service
            connector is required for this flavor.
        """
        return ServiceConnectorRequirements(
            connector_type=AWS_CONNECTOR_TYPE,
            resource_type=AWS_RESOURCE_TYPE,
        )

    @property
    def docs_url(self) -> Optional[str]:
        """A url to point at docs explaining this flavor.

        Returns:
            A flavor docs url.
        """
        return self.generate_default_docs_url()

    @property
    def sdk_docs_url(self) -> Optional[str]:
        """A url to point at SDK docs explaining this flavor.

        Returns:
            A flavor SDK docs url.
        """
        return self.generate_default_sdk_docs_url()

    @property
    def logo_url(self) -> str:
        """A url to represent the flavor in the dashboard.

        Returns:
            The flavor logo.
        """
        return "https://public-flavor-logos.s3.eu-central-1.amazonaws.com/image_builder/aws.png"

    @property
    def config_class(self) -> Type[BaseImageBuilderConfig]:
        """The config class.

        Returns:
            The config class.
        """
        return AWSImageBuilderConfig

    @property
    def implementation_class(self) -> Type["AWSImageBuilder"]:
        """Implementation class.

        Returns:
            The implementation class.
        """
        from zenml.integrations.aws.image_builders import AWSImageBuilder

        return AWSImageBuilder
