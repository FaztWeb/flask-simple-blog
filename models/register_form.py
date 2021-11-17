from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.simple import EmailField


class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=3, max=25)])
    email = EmailField("Email", [validators.Length(min=6, max=60)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Password do not match"),
        ],
    )
    confirm = PasswordField("Confirm Password")
