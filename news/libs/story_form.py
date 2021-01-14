from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import HiddenInput


class StoryForm(FlaskForm):
    method_type = StringField(widget=HiddenInput(), default="PATCH")
    story_title = StringField(
        label='Story Title',
        validators=[
            InputRequired(),
            Length(
                min=3,
                max=256,
                message=(
                    "must be between 3 and 256 characters long."
                ),
            ),
        ]
    )
    story_url = StringField(validators=[
        InputRequired(),
        Length(
                min=3,
                max=256,
                message="must be between 3 and 256 characters long.",
            ),
        ])
    story_text = TextAreaField(validators=[
        InputRequired(),
        Length(
                min=3,
                max=2048,
                message=(
                    "must be between 3 and 2048 characters long."
                ),
            ),
        ])
    edit_story_submit = SubmitField('Edit story')
