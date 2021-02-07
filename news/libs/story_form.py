from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import HiddenInput


class StoryForm(FlaskForm):
    story_form_method_type = StringField(widget=HiddenInput(), default="PATCH")
    story_title = StringField(
        label='Story Title',
        validators=[
            InputRequired(
                message='Story Title - This field is required.'
            ),
            Length(
                min=3,
                max=256,
                message=(
                    "Story Title - must be between 3 and 256 characters long."
                ),
            ),
        ]
    )
    story_url = StringField(validators=[
        InputRequired(
            message='Story Url - This field is required.'
        ),
        Length(
                min=3,
                max=256,
                message="Story Url - must be between 3 and "
                "256 characters long.",
            ),
        ])
    story_text = TextAreaField(validators=[
        InputRequired(
            message='Story Text - This field is required.'
        ),
        Length(
                min=3,
                max=2048,
                message=(
                    "Story Text - must be between 3 and 2048 characters long."
                ),
            ),
        ])
    edit_story_submit = SubmitField('Edit story')
