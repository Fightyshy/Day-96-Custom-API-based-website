from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
import bs4
import requests

from ..objects.char_claim_token import generate_token, confirm_token
from ..objects import const_loader
from ..models.models import PlayerCharacter, db
from ..objects.forms import (
    ClaimCharForm,
    LodestoneForm,
)

# load selectors and helpers
CHARACTER_SELECTORS = const_loader.CharacterData()
SERVERS = const_loader.Servers()

main_page = Blueprint("main_page", __name__, template_folder="templates")

# Enable only for testing
# @app.route("/test/<int:char_id>")
# def test(char_id):
#     # get_ffxiv_collect(5286865)
#     # return jsonify(get_ffxiv_collect(5286865))
#     # lodestone_achievement_scrape(5286865)
#     # retrieved = lodestone_achievement_scrape(char_id)
#     # final = [COLLECT_CACHE[2][int(id)] for id in retrieved]
#     # for entry in test:
#     #     for achieve in cached_achivements["results"]:
#     #         if achieve["id"]==int(entry):
#     #             final.append(achieve)
#     return jsonify({"test": cache.get("ffxiv_cached_resources")["mounts"]})

@main_page.route("/", methods=["GET", "POST"])
def get_charid():
    """Takes user lodestone url and any extra generation params"""
    lodestoneform = LodestoneForm()
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
    return render_template("index.html", form=lodestoneform)


@main_page.route("/auth", methods=["GET", "POST"])
def claim_charid():
    # In the future with a db, query first to see if char token exists, if it does, redirect and flash to index
    claimform = ClaimCharForm()
    token = request.args.get("token")
    # print(token, charid)
    if claimform.is_submitted():
        # retrieve charid
        charid = confirm_token(token, current_app)
        if charid is False:
            flash("Token has expired or was invalid.")
            return redirect(url_for("main_page.get_charid"))

        response = requests.get(
            f"https://na.finalfantasyxiv.com/lodestone/character/{charid}"
        )
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        char_prof = soup.select_one(".character__selfintroduction")
        retrieved = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==charid)).scalar()

        if retrieved:
            print("Exists already")
            flash("This character has already been claimed. If this was not done by you, please contact me to resolve this.")
            return render_template("authentication.html", form=claimform, token=token)
        elif char_prof.text != token:
            flash(
                "Text in character profile does not match. Please try again removing any extra text/spaces from your character profile, and inserting your confirmation code again.",
                "error",
            )
            return render_template(
                "authentication.html", form=claimform, token=token
            )
        else:
            print("Success")
            new_char = PlayerCharacter()
            new_char.char_id = charid
            db.session.add(new_char)
            db.session.commit()
            return redirect(url_for("retrieve_char_details", char_id=charid, mode="edit"))

    return render_template("authentication.html", form=claimform, token=token)
