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
        to: str = None,
        msg: str = None,
    ):
        """Initialize a new MessageDeliveryDetails."""
        self._to = to
        self._msg = msg

    @property
    def to(self) -> str:
        """Accessor for the to address of next cloud agent."""
        return self._to

    @property
    def msg(self) -> str:
        """Accessor for the encrypted message for next cloud agent."""
        return self._msg


class MessageDeliveryDetailsSchema(BaseModelSchema):
    """Schema to allow serialization/deserialization of wallet verification key."""

    class Meta:
        """MessageDeliveryDetailsSchema metadata."""

        model_class = MessageDeliveryDetails

    key = fields.Str(required=False)
