from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    HiddenField,
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
    URLField,
    SubmitField,
)
from wtforms.validators import DataRequired, URL, Length, NumberRange


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
        validators=[FileAllowed(["jpg", "png", "jpeg"], "JPG/PNG only")],
    )
    char_id_summary = HiddenField(validators=[DataRequired()])
    submit_char = SubmitField("Upload portrait")


class RoleplayPortraitForm(FlaskForm):
    portrait = FileField(
        "Upload portrait for RP here (otherwise it defaults to the Lodestone portrait)",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")],
    )
    char_id_rp = HiddenField(validators=[DataRequired()])
    submit_rp = SubmitField("Upload portrait")


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
    char_id_bs = HiddenField(validators=[DataRequired()])
    submit_business = SubmitField("Upload images and save layout")


class RPHookForm(FlaskForm):
    hook1_title = StringField(
        "Hook one header", validators=[DataRequired(), Length(min=0, max=35)]
    )
    hook1_body = TextAreaField(
        "Hook one content", validators=[DataRequired(), Length(min=0, max=240)]
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


class RPTraitsForm(FlaskForm):
    pos_trait1 = StringField(
        "Positive Trait one", validators=[DataRequired(), Length(min=0, max=20)]
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
        "Negative Trait one", validators=[DataRequired(), Length(min=0, max=20)]
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
        "Age", validators=[DataRequired(), NumberRange(min=1, max=10000)]
    )
    gender = StringField(
        "Gender", validators=[DataRequired(), Length(max=20)]
    )
    sexuality = StringField(
        "Sexuality", validators=[DataRequired(), Length(max=35)]
    )
    relationship = StringField(
        "Relationship Status", validators=[DataRequired(), Length(max=20)]
    )

    submit_char_summary = SubmitField("Save summary")


class RPCharNicknames(FlaskForm):
    nicknames = StringField("Nickname(s)", validators=[Length(min=0, max=20)])

    submit_nicknames = SubmitField("Save nickname(s)")


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
    notes = StringField("Notes", validators=[Length(max=90)])

    submit_socials = SubmitField("Save socials")


class RPOOCAboutMe(FlaskForm):
    aboutme = TextAreaField("About Me", validators=[Length(max=290)])
    submit_about_me = SubmitField("Save about me")
