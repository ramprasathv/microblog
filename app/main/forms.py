from flask_wtf import FlaskForm # Web forms
from wtforms import StringField, SubmitField, TextAreaField # Form elements
from wtforms.validators import DataRequired # Form field data validator
from wtforms.validators import ValidationError # raise ValidationError exception
from app.models import User # User model to validate the user/email fields
from wtforms.validators import Length # Check the length of the text field
from flask_babel import lazy_gettext as _1 # Strings Translation
from flask_babel import _ # Strings Translation
from flask import request # Request for the Search form

class EditProfileForm(FlaskForm):
    username = StringField(_1('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_1('About Me'), validators=[Length(min=0,max=140)])
    submit = SubmitField(_1('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    post = TextAreaField(_1('Say something'), validators=[
        DataRequired(), Length(min=1,max=140)])
    submit = SubmitField(_1('Submit'))

class SearchForm(FlaskForm):
    q = StringField(_1('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)