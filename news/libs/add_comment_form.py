from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField
from wtforms.validators import InputRequired


class AddCommentForm(FlaskForm):
    comment_deleted = HiddenField(default=False)
    existed_comment_id = HiddenField()
    existed_comment_text = HiddenField()
    comment_text = TextAreaField(validators=[InputRequired()])
