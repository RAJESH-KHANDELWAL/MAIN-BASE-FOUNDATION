
    def login_with_password(
        self,
        username: str,
        password: str,
    ):
        """Authenticate using Gmail ID or username and password."""

        identifier = username.strip()

        if not identifier or not password:
            return {
                "authenticated": False,
                "message": "Gmail ID or username and password are required",
            }

        # First, find the user by username.
        user = self.user_service.search_user_by_username(
            identifier
        )

        # If not found, try searching by email.
        if user is None:
            user = self.user_service.search_user_by_email(
                identifier
            )

        if user is None:
            return {
                "authenticated": False,
                "message": "Invalid Gmail ID or password",
            }

        if user.status != "ACTIVE":
            return {
                "authenticated": False,
                "message": "User account is not active",
            }

        verified = self.user_service.verify_user_password(
            user.username,
            password,
        )

        if not verified:
            return {
                "authenticated": False,
                "message": "Invalid Gmail ID or password",
            }

        identity = self.identity_service.search_identity(
            user.username
        )

        now = datetime.now(timezone.utc)
        created_at = now.isoformat()

        expires_at = (
            now + timedelta(
                hours=self.SESSION_DURATION_HOURS
            )
        ).isoformat()

        session_id = secrets.token_urlsafe(32)
        token = secrets.token_urlsafe(48)
        token_hash = self.hash_token(token)

        self.database_service.execute(
            """
            INSERT INTO auth_sessions (
                session_id,
                token_hash,
                username,
                status,
                created_at,
                expires_at,
                revoked_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                token_hash,
                user.username,
                "ACTIVE",
                created_at,
                expires_at,
                None,
                created_at,
            ),
        )

        return AuthenticationInfo(
            master_id=(
                identity.master_id
                if identity is not None
                else ""
            ),
            identity_id=(
                identity.identity_id
                if identity is not None
                else ""
            ),
            supreme_id=(
                identity.supreme_id
                if identity is not None
                else ""
            ),
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            phone=user.phone,
            authenticated=True,
            session_id=session_id,
            token=token,
            status=user.status,
            last_login=created_at,
            created_at=created_at,
            updated_at=created_at,
        )
