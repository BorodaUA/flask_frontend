from flask_jwt_extended import get_jwt_identity


def register_app_handlers(app):
    """
    The way to access app. from different file, for apphandlers etc.
    """

    @app.context_processor
    def user_uuid():
        """
        Global context processor that setting user_uuid from jwt_identity access_cookies.
        """
        current_user = get_jwt_identity()
        return dict(user_uuid=current_user)
