from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, IntegerField, TextField, BooleanField
from wtforms.validators import InputRequired
from wtforms.widgets import HiddenInput


class AddCommentForm(FlaskForm):
    method_type = TextField(widget=HiddenInput(), default='POST')
    comment_deleted = HiddenField(default=False)
    existed_comment_id = IntegerField(widget=HiddenInput(), default=0)
    existed_comment_text = TextField(widget=HiddenInput(), default='')
    comment_text = TextAreaField(validators=[InputRequired()])
