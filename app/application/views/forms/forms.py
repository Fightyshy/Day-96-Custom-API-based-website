import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    BooleanField,
    EmailField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
    URLField,
    SubmitField,
    ValidationError,
    PasswordField
)
from wtforms.validators import DataRequired, URL, Length, NumberRange
from ...objects.api_fetchers import SERVERS

MERGED_SERVERS = (
    SERVERS.get_jp() + SERVERS.get_NA() + SERVERS.get_EU() + SERVERS.get_OC()
)


class UserLogin(FlaskForm):
    char_id = StringField("Character ID", validators=[DataRequired(message="You need to enter a character id")])
    password = PasswordField("Password", validators=[DataRequired(message="You need to enter your password")])
    submit = SubmitField("Submit")

    def validate_char_id(self, field):
        if re.fullmatch("^[0-9]+$", field.data) is None:
            raise ValidationError("Character ID must only have numbers")


class UserRegistration(FlaskForm):
    email = EmailField("Email (We use this for recovery and support verification)", validators=[DataRequired("Please enter your email address")])
    password = PasswordField("Password (Must have one capital letter, number minimum, and be between 8-15 characters)", validators=[DataRequired("Please enter a password"), Length(8, 15)])
    repeat = PasswordField("Repeat password", validators=[DataRequired("Please enter your password again")])
    submit = SubmitField("Submit and claim character")

    def validate_password(self, field):
        if re.fullmatch(".*(?=.?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).*", field.data) is None and (len(field.data) < 7 and len(field.data) > 16):
            raise ValidationError("Password must contain 1 uppercase letter and 1 number, and must be between 8-15 characters")

    def validate_repeat(self, field):
        if self.password.data != field.data:
            raise ValidationError("Passwords do not match")


class PasswordReset(FlaskForm):
    char_id = StringField("Character ID", validators=[DataRequired(message="You need to enter the character id")])
    email = StringField("Email address of Character", validators=[DataRequired("Please enter the email associated with the character ID")])
    submit = SubmitField("Reset password")

    def validate_char_id(self, field):
        if re.fullmatch("^[0-9]+$", field.data) is None:
            raise ValidationError("Character ID must only have numbers")


class PasswordChange(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired("Please enter a new password")])
    repeat = PasswordField("Repeat password", validators=[DataRequired("Please enter your password again")])
    submit = SubmitField("Change password")

    def validate_password(self, field):
        if re.fullmatch(".*(?=.?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).*", field.data) is None and (len(field.data) < 7 and len(field.data) > 16):
            raise ValidationError("Password must contain 1 uppercase letter and 1 number, and must be between 8-15 characters")

    def validate_repeat(self, field):
        if self.password.data != field.data:
            raise ValidationError("Passwords do not match")


class LodestoneForm(FlaskForm):
    lodestone_url = URLField(
        "Lodestone URL: ", validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit")


class ClaimCharForm(FlaskForm):
    submit = SubmitField(
        "My token is in the character profile section on my Lodestone"
    )


class UploadPortraitForm(FlaskForm):
    portrait = FileField(
        "Upload custom portrait here (otherwise it defaults to the Lodestone portrait)",
        validators=[
            FileAllowed(["jpg", "png", "jpeg"], message="JPG/PNG only")
        ],
    )
    submit_char = SubmitField("Upload portrait")


class BusinessImages(FlaskForm):
    layout = SelectField(
        "Layout setting",
        choices=[
            ("1", "Two images only"),
            ("2", "Large image with name"),
            ("3", "Two images with name"),
        ],
        default="Two images only",
    )
    logo = FileField(
        "Upload logo or squarish image",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")],
    )
    venue = FileField(
        "Upload venue or 650x375 image",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")],
    )
    big_venue = FileField(
        "Upload venue or 1140x375 image",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")],
    )
    submit_business = SubmitField("Upload images and save layout")


class RPHookForm(FlaskForm):
    hook1_title = StringField(
        "Hook one header",
        validators=[
            DataRequired(message="You need to enter atleast the first set"),
            Length(min=0, max=35),
        ],
    )
    hook1_body = TextAreaField(
        "Hook one content",
        validators=[
            DataRequired(message="You need to enter atleast the first set"),
            Length(min=0, max=240),
        ],
    )

    hook2_title = StringField(
        "Hook two header", validators=[Length(min=0, max=35)]
    )
    hook2_body = TextAreaField(
        "Hook two content", validators=[Length(min=0, max=240)]
    )

    hook3_title = StringField(
        "Hook three header", validators=[Length(min=0, max=35)]
    )
    hook3_body = TextAreaField(
        "Hook three content", validators=[Length(min=0, max=240)]
    )

    submit_hooks = SubmitField("Save hooks")

    # dual field checkers, if one is filled but the other isn't, throw
    def validate_hook2_title(self, field):
        if len(field.data) >= 1 and len(self.hook2_body.data) == 0:
            raise ValidationError(
                "You need to fill in the content for hook 2 as well"
            )

    def validate_hook2_body(self, field):
        if len(field.data) >= 1 and len(self.hook2_title.data) == 0:
            raise ValidationError(
                "You need to fill in the title for hook 2 as well"
            )

    def validate_hook3_title(self, field):
        if len(field.data) >= 1 and len(self.hook3_body.data) == 0:
            raise ValidationError(
                "You need to fill in the content for hook 3 as well"
            )

    def validate_hook3_body(self, field):
        if len(field.data) >= 1 and len(self.hook3_title.data) == 0:
            raise ValidationError(
                "You need to fill in the title for hook 3 as well"
            )


class RPTraitsForm(FlaskForm):
    pos_trait1 = StringField(
        "Positive Trait one",
        validators=[
            DataRequired(message="You need to enter atleast the first set"),
            Length(min=0, max=20),
        ],
    )
    pos_trait2 = StringField(
        "Positive Trait two", validators=[Length(min=0, max=20)]
    )
    pos_trait3 = StringField(
        "Positive Trait three", validators=[Length(min=0, max=20)]
    )
    pos_trait4 = StringField(
        "Positive Trait four", validators=[Length(min=0, max=20)]
    )
    pos_trait5 = StringField(
        "Positive Trait five", validators=[Length(min=0, max=20)]
    )

    neg_trait1 = StringField(
        "Negative Trait one",
        validators=[
            DataRequired(message="You need to enter atleast the first set"),
            Length(min=0, max=20),
        ],
    )
    neg_trait2 = StringField(
        "Negative Trait two", validators=[Length(min=0, max=20)]
    )
    neg_trait3 = StringField(
        "Negative Trait three", validators=[Length(min=0, max=20)]
    )
    neg_trait4 = StringField(
        "Negative Trait four", validators=[Length(min=0, max=20)]
    )
    neg_trait5 = StringField(
        "Negative Trait five", validators=[Length(min=0, max=20)]
    )

    submit_traits = SubmitField("Save traits")


class RPCharSummary(FlaskForm):
    age = IntegerField(
        "Age",
        validators=[
            DataRequired(message="Please enter the character's age"),
            NumberRange(
                min=1,
                max=10000,
                message="Age should be between 1-10000 (Don't be stupid)",
            ),
        ],
    )
    gender = StringField(
        "Gender",
        validators=[
            DataRequired(message="Please enter the character's gender"),
            Length(max=20),
        ],
    )
    sexuality = StringField(
        "Sexuality",
        validators=[
            DataRequired(message="Please enter the character's sexuality"),
            Length(max=35),
        ],
    )
    relationship = StringField(
        "Relationship Status",
        validators=[
            DataRequired(
                message="Please enter the character's relationship status"
            ),
            Length(max=20),
        ],
    )

    submit_char_summary = SubmitField("Save summary")


class RPCharAlias(FlaskForm):
    alias = StringField("Nickname(s)", validators=[Length(min=0, max=20)])

    submit_alias = SubmitField("Save nickname(s)")


class RPCharQuote(FlaskForm):
    quote = StringField("Quote/Tagline", validators=[Length(min=0, max=50)])

    submit_char_quote = SubmitField("Save character quote")


class RPOOCSocials(FlaskForm):
    twitter = StringField("Twitter", validators=[Length(max=15)])
    website = StringField(
        "Website (Please use a shortener it's over 40 characters!):",
        validators=[Length(max=40)],
    )
    discord = StringField("Discord", validators=[Length(max=32)])
    oc_notes = StringField("Notes", validators=[Length(max=90)])

    submit_socials = SubmitField("Save socials")


class RPOOCAboutMe(FlaskForm):
    about_me = TextAreaField("About Me", validators=[Length(max=290)])
    submit_about_me = SubmitField("Save about me")


class VenueNameAndTagline(FlaskForm):
    venue_name = StringField(
        "Name", validators=[DataRequired(), Length(max=25)]
    )
    venue_tagline = StringField("Tagline", validators=[Length(max=40)])

    submit_venue_name = SubmitField("Save venue name/tagline")


class VenuePlotAddress(FlaskForm):
    housing_zone = SelectField(
        "Housing zone",
        choices=[
            "The Mist",
            "The Lavender Beds",
            "The Goblet",
            "Shirogane",
            "The Firmament",
        ],
        default="The Mist",
        validators=[
            DataRequired(message="You must select the venue's housing zone")
        ],
    )

    # Transform into switch frontend
    is_apartment = BooleanField("Is it a apartment or plot?")

    housing_ward = SelectField(
        "Ward No.",
        choices=[(0, "Choose...")] + [(i, i) for i in range(1, 25)],
        validators=[DataRequired(message="You must select a ward")],
        default=0,
        coerce=int,
    )

    # Either or for these ones
    ward_plot = SelectField(
        "Plot No.",
        choices=[(0, "Choose...")] + [(j, j) for j in range(1, 61)],
        default=0,
        coerce=int,
    )

    apartment_num = SelectField(
        "Apartment No.",
        choices=[(0, "Choose...")] + [(k, k) for k in range(1, 91)],
        default=0,
        coerce=int,
    )

    server = SelectField(
        "Server",
        choices=["Choose..."]
        + [item["server-name"] for item in MERGED_SERVERS],
        default="Choose...",
    )

    def validate_ward_plot(self, field):
        if not self.is_apartment.data and field.data == 0:
            raise ValidationError("You must select a plot")

    def validate_apartment_num(self, field):
        if self.is_apartment.data and field.data == 0:
            raise ValidationError("You must select a apartment")

    def validate_server(self, field):
        if field.data == "Choose...":
            raise ValidationError("You must select your venue's server")


class VenueContactAndSocials(VenuePlotAddress):
    # address = FormField(VenuePlotAddress)

    venue_operating_times = StringField("Operating hours")
    venue_twitter = StringField("Twitter", validators=[Length(max=15)])
    venue_discord = StringField("Discord", validators=[Length(max=32)])
    venue_website = StringField(
        "Website (Please use a shortener if it's over 40 characters!):",
        validators=[Length(max=40)],
    )
    submit_venue_contact = SubmitField("Save venue contacts and socials")


class VenueStaffDetails(FlaskForm):
    staff_role = StringField(
        "Role at venue",
        validators=[
            DataRequired(
                message="Please enter your role at the venue you work/own at"
            ),
            Length(min=1, max=50),
        ],
    )
    staff_twitter = StringField("Twitter", validators=[Length(max=15)])
    staff_discord = StringField("Discord", validators=[Length(max=32)])
    staff_website = StringField(
        "Website (Please use a shortener if it's over 40 characters!):",
        validators=[Length(max=40)],
    )

    submit_staff_details = SubmitField("Save own details")
