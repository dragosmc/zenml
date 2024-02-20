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
"""Collection of all models concerning actions."""
import copy
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import Field

from zenml.constants import STR_FIELD_MAX_LENGTH
from zenml.enums import PluginSubType
from zenml.models.v2.base.base import BaseZenModel
from zenml.models.v2.base.scoped import (
    WorkspaceScopedFilter,
    WorkspaceScopedRequest,
    WorkspaceScopedResponse,
    WorkspaceScopedResponseBody,
    WorkspaceScopedResponseMetadata,
    WorkspaceScopedResponseResources,
)

if TYPE_CHECKING:
    from zenml.models.v2.core.trigger import TriggerResponse
    from zenml.zen_stores.schemas import BaseSchema

    AnySchema = TypeVar("AnySchema", bound=BaseSchema)


# ------------------ Request Model ------------------


class ActionRequest(WorkspaceScopedRequest):
    """Model for creating a new action."""

    name: str = Field(
        title="The name of the action.", max_length=STR_FIELD_MAX_LENGTH
    )
    description: str = Field(
        default="",
        title="The description of the action",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    flavor: str = Field(
        title="The flavor of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_subtype: PluginSubType = Field(
        title="The subtype of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    configuration: Dict[str, Any] = Field(
        title="The configuration for the action.",
    )


# ------------------ Update Model ------------------


class ActionUpdate(BaseZenModel):
    """Update model for actions."""

    name: Optional[str] = Field(
        default=None,
        title="The new name for the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        default=None,
        title="The new description for the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    configuration: Optional[Dict[str, Any]] = Field(
        default=None,
        title="The configuration for the action.",
    )

    @classmethod
    def from_response(cls, response: "ActionResponse") -> "ActionUpdate":
        """Create an update model from a response model.

        Args:
            response: The response model to create the update model from.

        Returns:
            The update model.
        """
        return ActionUpdate(
            configuration=copy.deepcopy(response.configuration),
        )


# ------------------ Response Model ------------------


class ActionResponseBody(WorkspaceScopedResponseBody):
    """Response body for actions."""

    flavor: str = Field(
        title="The flavor of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    plugin_subtype: str = Field(
        title="The subtype of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )


class ActionResponseMetadata(WorkspaceScopedResponseMetadata):
    """Response metadata for actions."""

    description: str = Field(
        default="",
        title="The description of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )
    configuration: Dict[str, Any] = Field(
        title="The configuration for the action.",
    )


class ActionResponseResources(WorkspaceScopedResponseResources):
    """Class for all resource models associated with the action entity."""

    # TODO: convert this to a Page when it no longer breaks the OpenAPI docs
    triggers: List["TriggerResponse"] = Field(
        title="The trigger associated with the action.",
    )


class ActionResponse(
    WorkspaceScopedResponse[
        ActionResponseBody, ActionResponseMetadata, ActionResponseResources
    ]
):
    """Response model for actions."""

    name: str = Field(
        title="The name of the action.",
        max_length=STR_FIELD_MAX_LENGTH,
    )

    def get_hydrated_version(self) -> "ActionResponse":
        """Get the hydrated version of this action.

        Returns:
            An instance of the same entity with the metadata field attached.
        """
        from zenml.client import Client

        return Client().zen_store.get_action(self.id)

    # Body and metadata properties
    @property
    def flavor(self) -> str:
        """The `flavor` property.

        Returns:
            the value of the property.
        """
        return self.get_body().flavor

    @property
    def plugin_subtype(self) -> PluginSubType:
        """The `plugin_subtype` property.

        Returns:
            the value of the property.
        """
        return self.get_body().plugin_subtype

    @property
    def description(self) -> str:
        """The `description` property.

        Returns:
            the value of the property.
        """
        return self.get_metadata().description

    @property
    def configuration(self) -> Dict[str, Any]:
        """The `configuration` property.

        Returns:
            the value of the property.
        """
        return self.get_metadata().configuration

    def set_configuration(self, configuration: Dict[str, Any]) -> None:
        """Set the `configuration` property.

        Args:
            configuration: The value to set.
        """
        self.get_metadata().configuration = configuration

    # Resource properties
    @property
    def triggers(self) -> List["TriggerResponse"]:
        """The `triggers` property.

        Returns:
            the value of the property.
        """
        return self.get_resources().triggers


# ------------------ Filter Model ------------------


class ActionFilter(WorkspaceScopedFilter):
    """Model to enable advanced filtering of all actions."""

    name: Optional[str] = Field(
        default=None,
        description="Name of the action.",
    )
    flavor: Optional[str] = Field(
        default=None,
        title="The flavor of the action.",
    )
    plugin_subtype: Optional[str] = Field(
        default=None,
        title="The subtype of the action.",
    )
    # TODO: Ignore these in normal filter and handle in sqlzenstore
    resource_id: Optional[Union[UUID, str]] = Field(
        default=None,
        description="By the resource this action references.",
    )
    resource_type: Optional[str] = Field(
        default=None,
        description="By the resource type this action references.",
    )
