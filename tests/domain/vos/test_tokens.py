import datetime
from uuid import UUID

import jwt

from app.domain.vos.tokens import AccessToken, CreateTokenPayload, RefreshToken, Token


def test_create_success():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
        token_type="access",
    )

    assert token.payload.sub == "user_id_123"
    assert token.payload.type == "access"
    assert isinstance(token.payload.jti, str)
    assert UUID(token.payload.jti)  # Validate that jti is a valid UUID


def test_decode_success():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
        token_type="access",
    )

    token_str = token.__str__()

    decoded_payload = Token.decode(token_str)

    print(decoded_payload)

    assert decoded_payload.sub == "user_id_123"
    assert decoded_payload.type == "access"
    assert decoded_payload.jti == token.payload.jti


def test_decode_invalid_token():
    invalid_token_str = "invalid.token.string"

    try:
        res = Token.decode(invalid_token_str)

        print(res)
        assert False, "Decoding should have failed for an invalid token"
    except jwt.DecodeError:
        pass  # Expected exception


def test_token_expiration():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(seconds=-1),
        ),
        token_type="access",
    )

    token_str = token.__str__()

    try:
        Token.decode(token_str)
        assert False, "Token should have expired"
    except jwt.ExpiredSignatureError:
        pass  # Expected exception


def test_token_invalid_signature():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
        token_type="access",
    )

    token_str = token.__str__()

    # Tamper with the token to invalidate the signature
    tampered_token_str = token_str + "tampered"

    try:
        Token.decode(tampered_token_str)
        assert False, "Token should have invalid signature"
    except jwt.InvalidSignatureError:
        pass  # Expected exception


def test_access_token():
    access_token = AccessToken(sub="user_id_123")

    assert access_token.payload.type == "access"


def test_refresh_token():
    refresh_token = RefreshToken(sub="user_id_123")

    assert refresh_token.payload.type == "refresh"
