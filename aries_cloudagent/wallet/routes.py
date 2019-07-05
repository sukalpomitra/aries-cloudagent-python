"""Connection handling admin routes."""

from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema

from marshmallow import fields, Schema

from .models.wallet_verification_key import WalletVerificationKeySchema
from .models.message_delivery_details import MessageDeliveryDetailsSchema

from .manager import WalletManager


class VerificationKeySchema(Schema):
    """Result schema for getting verification key."""

    results = fields.List(fields.Nested(WalletVerificationKeySchema()))


@docs(
    tags=["wallet"],
    summary="Cloud agent verification key",
    parameters=[],
)


@docs(tags=["wallet"], summary="Get verification key")
@response_schema(VerificationKeySchema(), 200)
async def get_verification_key(request: web.BaseRequest):
    """
    Request handler for getting cloud agent verification key.

    Args:
        request: aiohttp request object

    Returns:
        The verification key

    """
    context = request.app["request_context"]

    seed = request.match_info["id"]
    wallet_mgr = WalletManager(context)
    walletverificationkey = await wallet_mgr.get_verification_key(seed)
    result = {
        "key": walletverificationkey.key,
    }
    return web.json_response(result)

@docs(tags=["wallet"], summary="Get message delivery details")
@response_schema(MessageDeliveryDetailsSchema(), 200)
async def get_message_delivery_details(request: web.BaseRequest):
    """
    Request handler for unpacking and getting forward details.

    Args:
        request: aiohttp request object

    Returns:
        The verification key

    """
    print("Unpacking message")
    body = await request.read()
    context = request.app["request_context"]
    wallet_mgr = WalletManager(context)
    messagedeliverydetails = await wallet_mgr.get_message_delivery_details(body)
    result = {
        "to": messagedeliverydetails.to,
        "msg": messagedeliverydetails.msg
    }
    print("Result:- " + messagedeliverydetails.to + " " + messagedeliverydetails.msg)
    return web.json_response(result)


async def register(app: web.Application):
    """Register routes."""

    app.add_routes(
        [
            web.get("/wallet/{id}", get_verification_key),
            web.post("/wallet/unpack", get_message_delivery_details),
        ]
    )
