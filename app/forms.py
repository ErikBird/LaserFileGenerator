from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import InputRequired

class PhonecaseForm(Form):
    height = StringField('height',validators=[InputRequired()])
    width = StringField('width',validators=[InputRequired()])
    depth = StringField('depth',validators=[InputRequired()])#, [validators.Regexp(r'^\d{1,4}\.?\d*$',message='Must be a number')]
    text = StringField('text',[validators.Length(min=0, max=22)])#[validators.Length(min=0, max=22)]

class WatchstrapForm(Form):
    top = StringField('top',validators=[InputRequired()])
    version = StringField('top', validators=[InputRequired()])
    buckle = StringField('buckle',validators=[InputRequired()])
    length = StringField('length',validators=[InputRequired()])
    nail = StringField('nail')
    text = StringField('text',[validators.Length(min=0, max=22)])

class WalletForm(Form):
    version = StringField('version',validators=[InputRequired()])
    text = StringField('text',[validators.Length(min=0, max=22)])

class TextForm(Form):
    text = StringField('text',[validators.Length(min=0, max=22)])