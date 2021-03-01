from flask_jwt_extended import get_jwt_identity, get_jwt_claims


def register_app_handlers(app):
    """
    The way to access app. from different file, for apphandlers etc.
    """

    @app.context_processor
    def user_uuid():
        """
        Global context processor that setting user_uuid
        from jwt_identity access_cookies.
        """
        current_user = get_jwt_identity()
        try:
            user_origin = get_jwt_claims()["user_origin"]
        except KeyError:
            user_origin = None
        try:
            user_uuid = get_jwt_claims()["user_uuid"]
        except KeyError:
            user_uuid = None
        return dict(
            username=current_user,
            user_origin=user_origin,
            user_uuid=user_uuid,
        )
