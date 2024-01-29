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
"""Abstract Schedule class that all Schedule event sources must implement."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Type

from zenml.enums import PluginSubType
from zenml.event_sources.base_event_source_plugin import (
    BaseEvent,
    BaseEventSourcePlugin,
    BaseEventSourcePluginFlavor,
    EventFilterConfig,
    EventSourceConfig,
)
from zenml.logger import get_logger
from zenml.models import EventSourceRequest, EventSourceResponse

logger = get_logger(__name__)

if TYPE_CHECKING:
    pass


# -------------------- Event Models -----------------------------------


class BaseScheduleEvent(BaseEvent):
    """Base class for all schedule events."""


# -------------------- Configuration Models ----------------------------------


class ScheduleEventSourceConfig(EventSourceConfig):
    """The Event Source configuration."""


class ScheduleEventFilterConfig(EventFilterConfig):
    """The Event Filter configuration."""


# -------------------- Plugin -----------------------------------


class BaseScheduleEventSourcePlugin(BaseEventSourcePlugin, ABC):
    """Base implementation for all Webhook event sources."""

    @property
    @abstractmethod
    def config_class(self) -> Type[ScheduleEventSourceConfig]:
        """Returns the `BasePluginConfig` config.

        Returns:
            The configuration.
        """

    def _create_event_source(
        self, event_source: EventSourceRequest
    ) -> EventSourceResponse:
        """Wraps the zen_store creation method to add plugin specific functionality."""
        # Implementations will be able to actually configure an external CronJobs
        #  before storing them in the database
        created_event_source = self.zen_store.create_event_source(
            event_source=event_source
        )
        return created_event_source


# -------------------- Flavors ----------------------------------


class BaseScheduleEventSourcePluginFlavor(BaseEventSourcePluginFlavor, ABC):
    """Base Event Plugin Flavor to access an event plugin along with its configurations."""

    SUBTYPE: ClassVar[PluginSubType] = PluginSubType.SCHEDULE
