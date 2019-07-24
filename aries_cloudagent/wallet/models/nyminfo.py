"""Handle connection information interface with non-secrets storage."""

import json
import uuid

from typing import Sequence

from marshmallow import fields

from ...config.injection_context import InjectionContext

from .base import BaseModel, BaseModelSchema


class NymInfo(BaseModel):
    """Represents the public did."""

    class Meta:
        """NymInfo metadata."""

        schema_class = "NymInfo"

    def __init__(
        self,
        *,
        did: str = None,
    ):
        """Initialize a new NymInfo."""
        self._id = did

    @property
    def did(self) -> str:
        """Accessor for the public did associated with this wallet."""
        return self._id


class NymInfoSchema(BaseModelSchema):
    """Schema to allow serialization/deserialization of wallet public did."""

    class Meta:
        """NymInfoSchema metadata."""

        model_class = NymInfo

    key = fields.Str(required=False)
