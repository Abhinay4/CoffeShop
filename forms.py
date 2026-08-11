from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Optional,
    ValidationError,
)

from models import User


class RegistrationForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, message="Use at least 8 characters.")],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create account")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower().strip()).first():
            raise ValidationError("An account with that email already exists.")


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Keep me signed in")
    submit = SubmitField("Log in")


class ProfileForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    save = SubmitField("Save changes")

    def __init__(self, original_email=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = (original_email or "").lower().strip()

    def validate_email(self, field):
        normalized = field.data.lower().strip()
        if normalized != self.original_email and User.query.filter_by(email=normalized).first():
            raise ValidationError("An account with that email already exists.")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired()],
    )
    new_password = PasswordField(
        "New password",
        validators=[DataRequired(), Length(min=8, message="Use at least 8 characters.")],
    )
    confirm_new_password = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match.")],
    )
    change_password = SubmitField("Update password")


class CheckoutForm(FlaskForm):
    full_name = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    phone = StringField(
        "Phone number",
        validators=[DataRequired(), Length(min=7, max=20)],
    )
    address_line1 = StringField(
        "Address",
        validators=[DataRequired(), Length(max=200)],
    )
    address_line2 = StringField(
        "Apartment, suite, etc. (optional)",
        validators=[Optional(), Length(max=200)],
    )
    city = StringField("City", validators=[DataRequired(), Length(max=100)])
    state = StringField("State", validators=[DataRequired(), Length(max=100)])
    postal_code = StringField(
        "PIN code",
        validators=[DataRequired(), Length(min=4, max=12)],
    )
    payment_method = RadioField(
        "Payment method",
        choices=[
            ("card", "Credit / Debit card"),
            ("upi", "UPI"),
            ("cod", "Cash on delivery"),
        ],
        default="card",
        validators=[DataRequired()],
    )
    submit = SubmitField("Place order")
