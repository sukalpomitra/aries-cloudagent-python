"""Classes to manage connections."""

import aiohttp
import logging
import sys

from typing import Union
from ..error import BaseError
from .error import WalletError
from ..messaging.error import MessageParseError
from ..config.injection_context import InjectionContext
from ..config.base import InjectorError
from .base import BaseWallet
from .models.wallet_verification_key import WalletVerificationKey
from .models.message_delivery_details import MessageDeliveryDetails

LOGGER = logging.getLogger(__name__)


class WalletManagerError(BaseError):
    """Wallet Manager error."""


class WalletManager:
    """Class for managing wallet."""

    def __init__(self, context: InjectionContext):
        """
        Initialize a ConnectionManager.

        Args:
            context: The context for this connection manager
        """
        self._context = context
        self._logger = logging.getLogger(__name__)

    def _log_state(self, msg: str, params: dict = None):
        """Print a message with increased visibility (for testing)."""
        if self._context.settings.get("debug.connections"):
            print(msg, file=sys.stderr)
            if params:
                for k, v in params.items():
                    print(f"    {k}: {v}", file=sys.stderr)
            print(file=sys.stderr)

    @property
    def context(self) -> InjectionContext:
        """
        Accessor for the current injection context.

        Returns:
            The injection context for this connection manager

        """
        return self._context

    async def get_verification_key(
        self,
        seed: str = None,
    ) -> WalletVerificationKey:
        """
        Gets the verification key of the wallet

        """
        self._log_state("Fetching key")

        # Create and store new invitation key
        wallet: BaseWallet = await self.context.inject(BaseWallet)
        connection_key = await wallet.create_signing_key(seed)
        print("Fetching key: " + connection_key.verkey)
        # Create connection record
        walletverificationkey = WalletVerificationKey(
            key=connection_key.verkey,
        )

        self._log_state(
            "Fetched Verification Key",
        )

        return walletverificationkey

    async def get_message_delivery_details(
            self,
            message_body: Union[str, bytes],
    ) -> MessageDeliveryDetails:
        """
        Unpacks message and gets the forwarding address for the next cloud agent

        """
        self._log_state("Unpacking Message")

        try:
            wallet: BaseWallet = await self.context.inject(BaseWallet)
        except InjectorError:
            raise MessageParseError("Wallet not defined in request context")

        try:
            unpacked = await wallet.unpack_message(message_body)
            message_json, sender_verkey, recipient_verkey = (
                unpacked
            )
        except WalletError:
            LOGGER.debug("Message unpack failed, falling back to JSON")

        self._log_state(
            "Fetched Message Delivery Details",
        )
        print(message_json)

        return None