from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import HiddenField, SelectField, URLField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL

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
    portrait = FileField("Upload custom portrait here (otherwise it defaults to the Lodestone portrait)", validators=[FileAllowed(["jpg", "png", "jpeg"], "JPG/PNG only")])
    char_id_summary = HiddenField(validators=[DataRequired()])
    submit_char = SubmitField(
        "Upload portrait"
    )

class RoleplayPortraitForm(FlaskForm):
    portrait = FileField("Upload portrait for RP here (otherwise it defaults to the Lodestone portrait)", validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")])
    char_id_rp = HiddenField(validators=[DataRequired()])
    submit_rp = SubmitField(
        "Upload portrait"
    )

class BusinessImages(FlaskForm):
    layout = SelectField("Layout setting", choices=["Two images only", "Large image with name", "Two images with name"], default="Two images only")
    logo = FileField("Upload logo or squarish image", validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")])
    venue = FileField("Upload venue or 650x375 image", validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")])
    big_venue = FileField("Upload venue or 1140x375 image", validators=[FileAllowed(["jpg", "jpeg", "png"], "JPG/PNG only")])
    char_id_bs = HiddenField(validators=[DataRequired()])
    submit_business = SubmitField(
        "Upload images and save layout"
    )