import dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from api_fetchers import get_fflogs_token, get_fflogs_character, cache
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, FileField
from wtforms.validators import DataRequired, URL
import bs4
from api_fetchers import (
    get_fflogs_character,
    get_fflogs_token,
    get_lodestone_char_basic,
    merge_raids,
)
import requests
import os
from char_claim_token import generate_token, confirm_token
import const_loader

# load selectors and helpers
CHARACTER_SELECTORS = const_loader.CharacterData()
SERVERS = const_loader.Servers()

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["CSRF"]
app.config["SECURITY_PASSWORD_SALT"] = os.environ["TOKEN_SALT"]
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
Bootstrap5(app)
cache.init_app(app)


class LodestoneForm(FlaskForm):
    lodestone_url = URLField(
        "Lodestone URL: ", validators=[DataRequired(), URL()]
    )
    submit = SubmitField("Submit")


class ClaimCharForm(FlaskForm):
    submit = SubmitField(
        "My token is in the character profile section on my Lodestone"
    )


# TODO another form for image and other things


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/", methods=["GET", "POST"])
def get_charid():
    """Takes user lodestone url and any extra generation params"""
    lodestoneform = LodestoneForm()
    if lodestoneform.validate_on_submit():
        # We want two things
        # The charid - leave as str
        lodestone_id = lodestoneform.lodestone_url.data.strip().split("/")[-2]
        # And a char token for uniquely identifying the user, made from the charid
        char_token = generate_token(lodestone_id, app)
        # interrupt here and present user with redirect to new page for first time auth
        # how to onepage another route here in a popup?
        # because popup
        # if check_password_hash(char_token) not in database
        return redirect(url_for("claim_charid", token=char_token))
        # else
        # get existing page that matched with check and redirect to editting page
    return render_template("index.html", form=lodestoneform)


@app.route("/auth", methods=["GET", "POST"])
def claim_charid():
    # In the future with a db, query first to see if char token exists, if it does, redirect and flash to index
    claimform = ClaimCharForm()
    token = request.args.get("token")
    # print(token, charid)
    if claimform.is_submitted():
        # retrieve charid
        charid = confirm_token(token, app)
        if charid is False:
            flash("Token has expired or was invalid.")
            return redirect(url_for("get_charid"))

        response = requests.get(
            f"https://na.finalfantasyxiv.com/lodestone/character/{charid}"
        )
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        char_prof = soup.select_one(".character__selfintroduction")
        if char_prof.text == token:
            print("Success")
            return redirect(url_for("retrieve_char_details", charid=charid))
        else:
            flash(
                "Text in character profile does not match. Please try again removing any extra text/spaces from your character profile, and inserting your confirmation code again.",
                "error",
            )
            return render_template(
                "authentication.html", form=claimform, token=token
            )
    return render_template("authentication.html", form=claimform, token=token)


# Can't api char profile text field, might need to scrape from site as auth via key recieved?
@app.route("/character")
def retrieve_char_details():
    """Get all details of char from booth XIVAPI/Lodestone and FFLogs"""

    try:
        # Character's lodestone id
        lodestone_id = int(request.args.get("charid"))
        # Then we fetch lodestone data -> fflogs data (if exists)
        # TODO waiting for xivapi to fix their lodestone scraper endpoint
        retrieved_data = get_lodestone_char_basic(lodestone_id)
        # Fetch fflogs data
        retrieve_token = get_fflogs_token()
        retrieved_logs = get_fflogs_character(
            retrieve_token,
            retrieved_data.name,
            retrieved_data.dcserver[0],
            SERVERS.get_region(retrieved_data.dcserver[0]),
        )
        # Merge fflogs dict into char dict if not None, error message for no-logs still displays
        if retrieved_logs != None:
            retrieved_data.char_raids = merge_raids(retrieved_logs)

    except TypeError:
        return {
            "Status": "404",
            "Type": "TypeError",
            "Message": "Data input is incorrectly typed/formatted.",
        }
    except IndexError:
        return {
            "Status": "404",
            "Type": "IndexError",
            "Message": "Unable to acquire link from ID",
        }
    except ValueError:
        return {
            "Status": "404",
            "Type": "ValueError",
            "Message": "Value of data input is incorrect",
        }
    else:
        print(retrieved_data.to_dict())
        return render_template("card.html", character=retrieved_data.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
