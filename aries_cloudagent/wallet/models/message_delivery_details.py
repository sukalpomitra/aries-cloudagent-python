"""Handle connection information interface with non-secrets storage."""

import json
import uuid

from typing import Sequence

from marshmallow import fields

from ...config.injection_context import InjectionContext

from .base import BaseModel, BaseModelSchema


class MessageDeliveryDetails(BaseModel):
    """Represents the message forward details for the cloud agent."""

    class Meta:
        """MessageDeliveryDetails metadata."""

        schema_class = "MessageDeliveryDetails"

    def __init__(
        self,
        *,
        key: str = None,
    ):
        """Initialize a new MessageDeliveryDetails."""
        self._id = key

    @property
    def key(self) -> str:
        """Accessor for the verification key associated with this wallet."""
        return self._id


class MessageDeliveryDetailsSchema(BaseModelSchema):
    """Schema to allow serialization/deserialization of wallet verification key."""

    class Meta:
        """MessageDeliveryDetailsSchema metadata."""

        model_class = MessageDeliveryDetails

    key = fields.Str(required=False)
