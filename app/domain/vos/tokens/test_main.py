import datetime

import jwt

from .main import AccessToken, CreateTokenPayload, RefreshToken, Token


def test_token_vo():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
        token_type="access",
    )

    token_str = token.get()

    assert isinstance(token_str, str)
    assert len(token_str) > 0
    assert token.payload.sub == "user_id_123"
    assert token.payload.type == "access"
    assert token.payload.jti is not None


def test_token_decoding():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
        token_type="access",
    )

    token_str = token.get()

    decoded_payload = Token.decode(token_str)

    assert decoded_payload.sub == "user_id_123"
    assert decoded_payload.type == "access"
    assert decoded_payload.jti == token.payload.jti


def test_token_expiration():
    token = Token(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(seconds=-1),
        ),
        token_type="access",
    )

    token_str = token.get()

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

    token_str = token.get()

    # Tamper with the token to invalidate the signature
    tampered_token_str = token_str + "tampered"

    try:
        Token.decode(tampered_token_str)
        assert False, "Token should have invalid signature"
    except jwt.InvalidSignatureError:
        pass  # Expected exception


def test_access_token():
    access_token = AccessToken(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(minutes=15),
        ),
    )

    assert access_token.payload.type == "access"


def test_refresh_token():
    refresh_token = RefreshToken(
        payload=CreateTokenPayload(
            sub="user_id_123",
            duration=datetime.timedelta(days=7),
        ),
    )

    assert refresh_token.payload.type == "refresh"
