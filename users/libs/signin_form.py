from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField(
        "username",
        validators=[
            InputRequired(message="Username field is required."),
            Length(
                message="Username must be between 3 and 32 characters long.",
                min=3,
                max=32,
            ),
        ],
    )

    password = PasswordField(
        "password",
        validators=[
            InputRequired(message="Password field is required."),
            Length(
                message="Password must be between 3 and 32 characters long.",
                min=3,
                max=32,
            ),
        ],
    )
