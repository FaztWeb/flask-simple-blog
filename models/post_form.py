from wtforms import Form, StringField, TextAreaField, validators

class PostForm(Form):
    title = StringField("Title", [validators.Length(min=1, max=200)])
    content = TextAreaField("Content", [validators.Length(min=30)])
