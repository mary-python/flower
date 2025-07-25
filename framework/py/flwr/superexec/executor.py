# Copyright 2025 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Execute and monitor a Flower run."""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from subprocess import Popen
from typing import Optional

from flwr.common import ConfigRecord
from flwr.common.typing import UserConfig
from flwr.server.superlink.linkstate import LinkStateFactory
from flwr.supercore.ffs import FfsFactory


@dataclass
class RunTracker:
    """Track a Flower run (composed of a run_id and the associated process)."""

    run_id: int
    proc: Popen  # type: ignore
    logs: list[str] = field(default_factory=list)


class Executor(ABC):
    """Execute and monitor a Flower run."""

    @abstractmethod
    def initialize(
        self, linkstate_factory: LinkStateFactory, ffs_factory: FfsFactory
    ) -> None:
        """Initialize the executor with the necessary factories.

        This method sets up the executor by providing it with the factories required
        to access the LinkState and the Flower File Storage (FFS) in the SuperLink.

        Parameters
        ----------
        linkstate_factory : LinkStateFactory
            The factory to create access to the LinkState.
        ffs_factory : FfsFactory
            The factory to create access to the Flower File Storage (FFS).
        """

    @abstractmethod
    def set_config(
        self,
        config: UserConfig,
    ) -> None:
        """Register provided config as class attributes.

        Parameters
        ----------
        config : UserConfig
            A dictionary for configuration values.
        """

    @abstractmethod
    def start_run(
        self,
        fab_file: bytes,
        override_config: UserConfig,
        federation_options: ConfigRecord,
        flwr_aid: Optional[str],
    ) -> Optional[int]:
        """Start a run using the given Flower FAB ID and version.

        This method creates a new run on the SuperLink, returns its run_id
        and also starts the run execution.

        Parameters
        ----------
        fab_file : bytes
            The Flower App Bundle file bytes.
        override_config: UserConfig
            The config overrides dict sent by the user (using `flwr run`).
        federation_options: ConfigRecord
            The federation options sent by the user (using `flwr run`).
        flwr_aid : Optional[str]
            The Flower Account ID of the user starting the run, if authentication is
            enabled.

        Returns
        -------
        run_id : Optional[int]
            The run_id of the run created by the SuperLink, or `None` if it fails.
        """
