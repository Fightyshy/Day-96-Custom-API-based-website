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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user
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

# temp login init
login_manager = LoginManager()

main_page = Blueprint("main_page", __name__, template_folder="templates")


@main_page.route("/", methods=["GET", "POST"])
def get_charid():
    """Takes user lodestone url and any extra generation params"""
    lodestoneform = LodestoneForm()
    userform = UserLogin()
    if lodestoneform.validate_on_submit():
        # We want two things
        # The charid - leave as str
        lodestone_id = lodestoneform.lodestone_url.data.strip().split("/")[-2]
        # And a char token for uniquely identifying the user, made from the charid
        char_token = generate_token(lodestone_id, current_app)
        # interrupt here and present user with redirect to new page for first time auth
        # how to onepage another route here in a popup?
        # because popup
        # if check_password_hash(char_token) not in database
        return redirect(url_for("main_page.claim_charid", token=char_token))
        # else
        # get existing page that matched with check and redirect to editting page
    elif userform.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.char_id==userform.char_id.data)).scalar()
        if not result:
            flash("Character has not been claimed yet")
            return redirect(url_for("main_page.get_charid"))
        elif not check_password_hash(result.password, userform.password.data):
            flash("Wrong password")
            return redirect(url_for("main_page.get_charid"))
        else:
            login_user(result)
            return redirect(url_for("card_maker.retrieve_char_details", char_id=result.char_id, mode="edit"))
    return render_template("index.html", form=lodestoneform, userform=userform)
    # TODO user login form to template, handle in different blueprint

# TODO convert into a registration page, trigger reg the same time as form validation is happening
# TODO login if successful, handle failure in the same way as currently
@main_page.route("/auth", methods=["GET", "POST"])
def claim_charid():
    # In the future with a db, query first to see if char token exists, if it does, redirect and flash to index
    userform = UserRegistration()

    token = request.args.get("token")

    if userform.validate_on_submit():
        # retrieve charid, redirect if invalid
        charid = confirm_token(token, current_app)
        if charid is False:
            flash("Token has expired or was invalid.")
            return redirect(url_for("main_page.get_charid"))
        try:
            response = requests.get(
                f"https://na.finalfantasyxiv.com/lodestone/character/{charid}"
            )
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            char_prof = soup.select_one(".character__selfintroduction")
            retrieved = db.session.execute(db.select(User).where(User.char_id==charid)).scalar()
        except requests.HTTPError as error:
            return jsonify({
                "status": "400",
                "errorMsg": str(error)
            })
        else:
            if char_prof.text != token:
                flash(
                    "Token in character profile does not match provided token. Please check that you've copied it properly and that it's the ONLY thing in the character profile.",
                )
                return render_template(
                    "authentication.html", form=userform, token=token
                )
            elif retrieved:
                flash("This character has already been claimed. If this was not done by you, please contact me to resolve this.")
                return render_template("authentication.html", form=userform, token=token)
            else:
                new_business = Business()
                new_roleplaying = Roleplaying()
                new_char = PlayerCharacter()
                new_char.char_id = charid
                new_char.business = new_business
                new_char.roleplaying = new_roleplaying

                new_user = User()
                new_user.char_id = charid
                new_user.password = generate_password_hash(userform.password.data)
                new_user.email = userform.email.data
                new_user.character = new_char

                db.session.add(new_char)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for("card_maker.retrieve_char_details", char_id=charid, mode="edit"))
    elif userform.errors:
        return render_template("authentication.html", errors=userform.errors, form=userform, token=token)

    return render_template("authentication.html", form=userform, token=token)


@main_page.route("/logout")
def logout_char():
    logout_user()
    return redirect(url_for("main_page.get_charid"))
