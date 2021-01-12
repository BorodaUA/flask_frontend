from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import HiddenInput


class AddCommentForm(FlaskForm):
    method_type = TextField(widget=HiddenInput(), default="POST")
    comment_id = TextField(widget=HiddenInput())
    comment_text = TextAreaField(
        validators=[
            InputRequired(
                message='Comment text field is required.'
            ),
            Length(
                min=2,
                max=8192,
                message=(
                    'Comment text field must be between 2 and 8192 characters long.'
                )
            )
        ]
    )
