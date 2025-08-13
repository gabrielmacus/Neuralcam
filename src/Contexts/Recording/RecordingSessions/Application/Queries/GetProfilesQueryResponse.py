from dataclasses import dataclass
from typing import List

from src.Contexts.SharedKernel.Domain.MessageBus.QueryResponse import QueryResponse
from ..DTO.ProfileDTO import ProfileDTO


@dataclass(frozen=True)
class GetProfilesQueryResponse(QueryResponse):
    profiles: List[ProfileDTO]
