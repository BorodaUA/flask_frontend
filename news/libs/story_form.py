from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import HiddenInput


class StoryForm(FlaskForm):
    method_type = TextField(widget=HiddenInput(), default="PATCH")
    story_title = TextField(
        validators=[
            InputRequired(),
            Length(
                min=3,
                max=256,
                message=(
                    "Story Title must be between 3 and 256 characters long."
                ),
            ),
        ]
    )
    story_url = TextField(validators=[
        InputRequired(),
        Length(
                min=3,
                max=256,
                message="Story Url must be between 3 and 256 characters long.",
            ),
        ])
    story_text = TextAreaField(validators=[
        InputRequired(),
        Length(
                min=3,
                max=2048,
                message=(
                    "Story Text must be between 3 and 2048 characters long."
                ),
            ),
        ])
