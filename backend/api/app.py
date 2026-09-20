def _require_ai_store_actor(
    authorization: Optional[str]
) -> str:
    """
    Authenticate the caller using the existing authentication system.

    The caller must provide:
        Authorization: Bearer <token>

    The token is validated through AuthenticationService.
    The authenticated username becomes the current AI Store actor.
    """

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="AUTHORIZATION_REQUIRED"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="INVALID_AUTHORIZATION_HEADER"
        )

    token = authorization[len("Bearer "):].strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="EMPTY_AUTH_TOKEN"
        )

    result = authentication_service.validate_token(token)

    if not result.get("authenticated"):
        raise HTTPException(
            status_code=401,
            detail=result.get(
                "message",
                "INVALID_AUTHENTICATION_TOKEN"
            )
        )

    username = result.get("username")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="AUTHENTICATED_USERNAME_NOT_FOUND"
        )

    return username
