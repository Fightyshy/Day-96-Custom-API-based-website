import dotenv
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from api_fetchers import (
    ffxiv_cached_resources,
    get_collectibles,
    get_fflogs_token,
    get_fflogs_character,
    cache,
)
from flask_bootstrap import Bootstrap5
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
from werkzeug.utils import secure_filename

from forms import (
    BusinessImages,
    ClaimCharForm,
    LodestoneForm,
    RoleplayPortraitForm,
    UploadPortraitForm,
)

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

COLLECT_CACHE = ffxiv_cached_resources()
LEN_MOUNTS = len(COLLECT_CACHE["mounts"])
LEN_MINIONS = len(COLLECT_CACHE["minions"])
LEN_ACHIEVES = len(COLLECT_CACHE["achievements"])

# TODO another form for image and other things


@app.route("/test/<int:char_id>")
def test(char_id):
    # get_ffxiv_collect(5286865)
    # return jsonify(get_ffxiv_collect(5286865))
    # lodestone_achievement_scrape(5286865)
    # retrieved = lodestone_achievement_scrape(char_id)
    # final = [COLLECT_CACHE[2][int(id)] for id in retrieved]
    # for entry in test:
    #     for achieve in cached_achivements["results"]:
    #         if achieve["id"]==int(entry):
    #             final.append(achieve)
    return jsonify({"test": cache.get("ffxiv_cached_resources")["mounts"]})


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


@app.route("/character/portrait", methods=["POST"])
def upload_portrait():
    if request.method == "POST":
        print(request.form["source"])
        portraitform = UploadPortraitForm()
        if portraitform.validate():
            image = portraitform.portrait.data
            extension = image.filename.split(".")[-1]

            if request.form["source"] == "summary":
                # TODO get char_id and check against filename sans extension
                # TODO add new file using char_id as file name while preserving file format
                # May have to change in the future because O(n) could get expensive on a server
                for root, dirs, files in os.walk(
                    os.path.join(app.root_path, r"static\assets\uploaded-img")
                ):
                    for name in files:
                        print(name, root)
                        if name.split(".")[0] == str(
                            portraitform.char_id_summary.data
                        ):
                            print("working")
                            print(rf"{root}\{name}")
                            os.remove(rf"{root}\{name}")

                image.save(
                    os.path.join(
                        app.root_path,
                        "static/assets/uploaded-img/",
                        secure_filename(portraitform.char_id_summary.data)
                        + f".{extension}",
                    )
                )
                return jsonify(
                    {
                        "src": url_for(
                            "static",
                            filename="assets/uploaded-img/"
                            + secure_filename(portraitform.char_id_summary.data),
                        )
                        + f".{extension}"
                    }
                )
            elif request.form["source"] == "roleplay":
                for root, dirs, files in os.walk(
                    os.path.join(app.root_path, r"static\assets\uploaded-img")
                ):
                    for name in files:
                        print(name, root)
                        splitted = name.split(".")
                        if splitted[0] == str(portraitform.char_id_summary.data)+"_rp":
                            print("working")
                            print(rf"{root}\{splitted[0]}.{splitted[1]}")
                            os.remove(rf"{root}\{splitted[0]}.{splitted[1]}")

                image.save(
                    os.path.join(
                        app.root_path,
                        "static/assets/uploaded-img/",
                        secure_filename(portraitform.char_id_summary.data)
                        + f"_rp.{extension}",
                    )
                )
                return jsonify(
                    {
                        "src": url_for(
                            "static",
                            filename="assets/uploaded-img/"
                            + secure_filename(portraitform.char_id_summary.data),
                        )
                        + f"_rp.{extension}"
                    }
                )
    else:
        return jsonify({"test": "error"})


@app.route("/character")
def retrieve_char_details():
    """Get all details of char from booth XIVAPI/Lodestone and FFLogs"""
    portraitform = UploadPortraitForm()
    rpform = RoleplayPortraitForm()
    bsform = BusinessImages()
    try:
        # Character's lodestone id
        lodestone_id = int(request.args.get("charid"))
        portraitform.char_id_summary.data = lodestone_id
        src = {}
        for root, dirs, files in os.walk(
            os.path.join(app.root_path, r"static\assets\uploaded-img")
        ):
            for name in files:
                print(name, root)
                splitted = name.split(".")
                if splitted[0] == str(
                    portraitform.char_id_summary.data
                ):
                    print("setting summary")
                    print(rf"{root}\{name}")
                    src["avatar"] = url_for(
                        "static", filename=f"/assets/uploaded-img/{name}"
                    )                  
                elif splitted[0] == str(portraitform.char_id_summary.data)+"_rp":
                    print("setting rp")
                    print(rf"{root}\{splitted[0]}_rp.{splitted[1]}")
                    src["roleplay"] = url_for(
                        "static", filename=f"/assets/uploaded-img/{name}"
                    ) 

        # GET reqs/Scraper funcs
        # Character summary page data
        retrieved_data = get_lodestone_char_basic(lodestone_id)
        # Collectibles data (either from FFXIV Collect API or scrape name/id and use FFXIV Collect queries to populate)
        retrieve_collectibles = get_collectibles(lodestone_id)
        # Fetch FFLogs data and merge into single dict/json
        retrieve_token = get_fflogs_token()
        retrieved_logs = merge_raids(
            get_fflogs_character(
                retrieve_token,
                retrieved_data.name,
                retrieved_data.dcserver[0],
                SERVERS.get_region(retrieved_data.dcserver[0]),
            )
        )
    # except TypeError as error:
    #     return {
    #         "Status": "404",
    #         "Type": "TypeError",
    #         "Message": "Data input is incorrectly typed/formatted.",
    #     }
    except IndexError:
        return {
            "Status": "404",
            "Type": "IndexError",
            "Message": "Unable to acquire link from ID",
        }
    # except ValueError:
    #     return {
    #         "Status": "404",
    #         "Type": "ValueError",
    #         "Message": "Value of data input is incorrect",
    #     }
    else:
        # condition check edit mode or no
        nicknames = ["Test", "test", "test"]
        mode = request.args.get("mode")
        if mode == "edit":
            return render_template(
                "card.html",
                character=retrieved_data.to_dict(),
                raid=retrieved_logs.to_dict()
                if retrieved_logs is not None
                else None,
                collectible=retrieve_collectibles,
                form=portraitform,
                bsform=bsform,
                src=src,
                aliases=nicknames,
                is_edit=True,
            )
        elif mode == "view":
            return render_template(
                "card.html",
                character=retrieved_data.to_dict(),
                raid=retrieved_logs.to_dict()
                if retrieved_logs is not None
                else None,
                collectible=retrieve_collectibles,
                src=src,
                is_edit=False,
            )


if __name__ == "__main__":
    app.run(debug=True)
