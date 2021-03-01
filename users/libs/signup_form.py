from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class SignupForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Username is required."),
            Length(
                message="Username must be between 3 and 32 characters long.",
                min=3,
                max=32,
            ),
        ],
    )
    email_address = StringField(
        "Email address",
        validators=[
            InputRequired(message="Email address is required."),
            Length(
                message="Email must be between 3 and 64 characters long.",
                min=3,
                max=64,
            ),
            Email(message="Email is invalid."),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required."),
            Length(
                message="Password must be between 3 and 32 characters long.",
                min=3,
                max=32,
            ),
        ],
    )
