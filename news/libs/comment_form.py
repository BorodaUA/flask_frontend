from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput


class AddCommentForm(FlaskForm):
    method_type = TextField(widget=HiddenInput(), default="POST")
    comment_id = TextField(widget=HiddenInput())
    comment_text = TextAreaField(validators=[InputRequired()])
