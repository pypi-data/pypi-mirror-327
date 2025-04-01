from __future__ import annotations

import json
from typing import Optional, Any

from pydantic import (
    BaseModel,
    conlist,
    model_validator,
    ConfigDict,
    field_serializer,
)
from pathlib import Path

from .dataset import DatasetVersion
from .deriva_definitions import RID


class Workflow(BaseModel):
    """A specification of a workflow.  Must have a name, URI to the workflow instance, and a type.  The workflow type
    needs to be an existing-controlled vocabulary term.

    Attributes:
        name: The name of the workflow
        url: The URI to the workflow instance.  In most cases should be a GitHub URI to the code being executed.
        workflow_type: The type of the workflow.  Must be an existing controlled vocabulary term.
        version: The version of the workflow instance.  Should follow semantic versioning.
        description: A description of the workflow instance.  Can be in Markdown format.
    """

    name: str
    url: str
    workflow_type: str
    version: Optional[str] = None
    description: str = None


class DatasetSpec(BaseModel):
    """Represent a dataset_table in an execution configuration dataset_table list

    Attributes:
        rid (RID): A dataset_table RID
        materialize (bool): If False, do not materialize datasets, only download table data, no assets.  Defaults to True
        version (DatasetVersion): The version of the dataset.  Should follow semantic versioning.
    """

    rid: RID
    materialize: bool = True
    version: DatasetVersion

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    @classmethod
    def _check_bare_rid(cls, data: Any) -> dict[str, str | bool]:
        # If you are just given a string, assume it's a rid and put into dict for further validation.
        return {"rid": data} if isinstance(data, str) else data

    @field_serializer("version")
    def serialize_version(self, version: DatasetVersion) -> dict[str, Any]:
        return version.to_dict()


class ExecutionConfiguration(BaseModel):
    """Define the parameters that are used to configure a specific execution.

    Attributes:
        datasets: List of dataset_table RIDS, MINIDS for datasets to be downloaded prior to execution.  By default,
                     all  the datasets are materialized. However, if the assets associated with a dataset_table are not
                     needed, a dictionary that defines the rid and the materialization parameter for the
                     download_dataset_bag method can be specified, e.g.  datasets=[{'rid': RID, 'materialize': True}].
        assets: List of assets to be downloaded prior to execution.  The values must be RIDs in an asset table
        workflow: A workflow instance.  Must have a name, URI to the workflow instance, and a type.
        description: A description of the execution.  Can use Markdown format.
    """

    datasets: conlist(DatasetSpec) = []
    assets: list[RID | str] = []  # List of RIDs to model files.
    workflow: Workflow
    description: str = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @staticmethod
    def load_configuration(path: Path) -> ExecutionConfiguration:
        """Create a ExecutionConfiguration from a JSON configuration file.

        Args:
          path: File containing JSON version of execution configuration.

        Returns:
          An execution configuration whose values are loaded from the given file.
        """
        with open(path) as fd:
            config = json.load(fd)
        return ExecutionConfiguration.model_validate(config)
