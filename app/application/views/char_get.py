from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
import bs4
import requests
from sqlalchemy import and_

from ..views.auth import register_user
from ..objects.char_claim_token import generate_token, confirm_token
from ..objects import const_loader
from ..models.models import Business, PlayerCharacter, Roleplaying, User, db
from .forms.forms import (
    LodestoneForm,
    UserLogin,
    UserRegistration,
)

# load selectors and helpers
CHARACTER_SELECTORS = const_loader.CharacterData()
SERVERS = const_loader.Servers()

main_page = Blueprint("main_page", __name__, template_folder="templates")


@main_page.route("/", methods=["GET", "POST"])
def get_charid():
    """Takes user lodestone url and any extra generation params"""
    lodestoneform = LodestoneForm()
    userform = UserLogin()  # Login auth moved to auth blueprint, form for rendering
    if lodestoneform.validate_on_submit():
        # Retrieve lodestone char id and tokenise it. Send the token to char claims
        lodestone_id = lodestoneform.lodestone_url.data.strip().split("/")[-2]
        char_token = generate_token(lodestone_id, current_app)
        return redirect(url_for("main_page.claim_charid", token=char_token))
    return render_template("index.html", form=lodestoneform, userform=userform)


@main_page.route("/auth", methods=["GET", "POST"])
def claim_charid():
    userform = UserRegistration()
    token = request.args.get("token")
    if userform.validate_on_submit():
        try:
            char_id = confirm_token(token, current_app)
            response = requests.get(
                f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}"
            )
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            char_profile = soup.select_one(".character__selfintroduction")
        except requests.HTTPError as error:
            return jsonify({
                "status": "400",
                "errorMsg": str(error)
            })
        else:
            if char_profile.text != token:
                flash(
                    "Token in character profile does not match provided token. Please check that you've copied it properly and that it's the ONLY thing in the character profile.",
                )
                return render_template(
                    "authentication.html", form=userform, token=token
                )
            else:
                # send token instead
                registration_state = register_user(token, userform.email.data, userform.password.data)
                if registration_state is True:
                    return render_template("register_sent.html")
    return render_template("authentication.html", form=userform, token=token)
