"""Handle connection information interface with non-secrets storage."""

import json
import uuid

from typing import Sequence

from marshmallow import fields

from ...config.injection_context import InjectionContext

from .base import BaseModel, BaseModelSchema


class WalletVerificationKey(BaseModel):
    """Represents the verification key for the wallet."""

    class Meta:
        """WalletVerificationKey metadata."""

        schema_class = "WalletVerificationKey"

    def __init__(
        self,
        *,
        key: str = None,
    ):
        """Initialize a new WalletVerificationKey."""
        self._id = key

    @property
    def key(self) -> str:
        """Accessor for the verification key associated with this wallet."""
        return self._id


class WalletVerificationKeySchema(BaseModelSchema):
    """Schema to allow serialization/deserialization of wallet verification key."""

    class Meta:
        """WalletVerificationKeySchema metadata."""

        model_class = WalletVerificationKey

    key = fields.Str(required=False)
