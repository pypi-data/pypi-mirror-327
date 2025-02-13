from dataclasses import dataclass
from enum import Enum
from typing import Optional

from sagemaker_studio._openapi.models import (
    GetExecutionRequest,
    ListExecutionsRequest,
    StartExecutionRequest,
    StopExecutionRequest,
)
from sagemaker_studio.data_models import BaseClientConfig


class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return any(item.name == value for item in cls)


class Status(BaseEnum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


class SortBy(BaseEnum):
    NAME = "NAME"
    STATUS = "STATUS"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"


class SortOrder(BaseEnum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class ErrorType(BaseEnum):
    CLIENT_ERROR = "CLIENT_ERROR"
    SERVER_ERROR = "SERVER_ERROR"


class LocalExecutionTerminalStatusesWithOutputFiles(BaseEnum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class LocalExecutionStoppableStatuses(BaseEnum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"


class ThrottlingError(Exception):
    pass


class ServiceQuotaExceededError(Exception):
    pass


class InternalServerError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class ConflictError(Exception):
    """Raised when Updating or deleting a resource can cause an inconsistent state."""

    def __init__(self, message="An error occurred"):
        self.message = message
        super().__init__(self.message)


class ProblemJsonError(Exception):
    pass


class ValidationError(Exception):
    pass


class RequestError(Exception):
    def __init__(self, message, response=None):
        self.message = message
        self.response = response
        super().__init__(self.message)


class ExecutionClient:
    def get_execution(self, request: GetExecutionRequest):
        pass

    def list_executions(self, request: ListExecutionsRequest):
        pass

    def start_execution(self, request: StartExecutionRequest):
        pass

    def stop_execution(self, request: StopExecutionRequest):
        pass


@dataclass
class ExecutionConfig(BaseClientConfig):
    local: Optional[bool] = False
    local_execution_client: Optional[ExecutionClient] = None
    sagemaker_user_home: Optional[str] = None
    domain_identifier: Optional[str] = None
    project_identifier: Optional[str] = None
    datazone_stage: Optional[str] = None
    datazone_endpoint: Optional[str] = None
    datazone_environment_id: Optional[str] = None
    datazone_domain_region: Optional[str] = None
    project_s3_path: Optional[str] = None
