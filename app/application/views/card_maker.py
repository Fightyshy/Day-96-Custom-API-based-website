from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    url_for,
)
from ..objects.api_fetchers import (
    SERVERS,
    get_collectibles,
    get_fflogs_token,
    get_fflogs_character,
    get_lodestone_char_basic,
    merge_raids
)
import os
from werkzeug.utils import secure_filename
from ..models.models import PlayerCharacter, Roleplaying, db
from ..objects.forms import (
    BusinessImages,
    RPCharAlias,
    RPCharQuote,
    RPCharSummary,
    RPHookForm,
    RPOOCAboutMe,
    RPOOCSocials,
    RPTraitsForm,
    UploadPortraitForm,
    VenueContactAndSocials,
    VenueNameAndTagline,
    VenueStaffDetails,
)

card_maker = Blueprint("card_maker", __name__, template_folder="templates")

# TODO for uploaders, find object store service to send images too
@card_maker.route("/character/venue", methods=["POST"])
def upload_venue_images():
    if request.method == "POST":
        bs_form = BusinessImages()
        if bs_form.validate():
            if bs_form.layout.data == "1" or bs_form.layout.data == "3":
                img_one = bs_form.logo.data
                img_two = bs_form.venue.data

                extension_one = img_one.filename.split(".")[-1]
                extension_two = img_two.filename.split(".")[-1]

                # TODO upload both images and overwrite existing
                for root, dirs, files in os.walk(
                    os.path.join(current_app.root_path, r"static\assets\uploaded-img")
                ):
                    for name in files:
                        splitted = name.split(".")
                        print(name, root)
                        if splitted[0] == str(bs_form.char_id_bs.data)+"_venue_1":
                            print("working")
                            print(rf"{root}\{name}")
                            os.remove(rf"{root}\{name}")
                        elif splitted[0] == str(bs_form.char_id_bs.data)+"_venue_2":
                            print("working")
                            print(rf"{root}\{name}")
                            os.remove(rf"{root}\{name}")

                # TODO images named name_venue_1.extension and name_venue_2.extension
                # TODO save and name like in portrait updating
                img_one.save(
                    os.path.join(
                        current_app.root_path,
                        "static/assets/uploaded-img/",
                        secure_filename(bs_form.char_id_bs.data)
                        + f"_venue_1.{extension_one}",
                    )
                )

                img_two.save(
                    os.path.join(
                        current_app.root_path,
                        "static/assets/uploaded-img/",
                        secure_filename(bs_form.char_id_bs.data)
                        + f"_venue_2.{extension_two}",
                    )
                )

                # TODO JSON response similar to portrait updating
                return jsonify({
                    "uploaded": "two",
                    "src": {
                        "one": url_for("static", filename="assets/uploaded-img/"+secure_filename(bs_form.char_id_bs.data)+ f"_venue_1.{extension_one}"),
                        "two": url_for("static", filename="assets/uploaded-img/"+secure_filename(bs_form.char_id_bs.data)+ f"_venue_2.{extension_two}")
                    }
                })
            elif bs_form.layout.data == "2":
                # TODO upload big image and overwrite exising
                img_big = bs_form.big_venue.data
                extension = img_big.filename.split(".")[-1]

                for root, dirs, files in os.walk(
                    os.path.join(current_app.root_path, r"static\assets\uploaded-img")
                ):
                    for name in files:
                        splitted = name.split(".")
                        print(name, root)
                        if splitted[0] == str(bs_form.char_id_bs.data)+"_venue_big":
                            print("working")
                            print(rf"{root}\{name}")
                            os.remove(rf"{root}\{name}")

                # TODO images named name_venue_big.extension
                # TODO save and name like in portrait updating
                img_big.save(
                    os.path.join(
                        current_app.root_path,
                        "static/assets/uploaded-img/",
                        secure_filename(bs_form.char_id_bs.data)
                        + f"_venue_big.{extension}",
                    )
                )

                # TODO JSON response similar to portrait updating
                return jsonify({
                    "uploaded": "big",
                    "src": url_for("static", filename="assets/uploaded-img/"+secure_filename(bs_form.char_id_bs.data)+ f"_venue_big.{extension}")
                })
    return jsonify({"test": "error"})

# TODO for uploaders, find object store service to send images too
# TODO revert to default Lodestone
@card_maker.route("/character/portrait", methods=["POST"])
def upload_portrait():
    if request.method == "POST":
        portraitform = UploadPortraitForm()
        if portraitform.validate():
            image = portraitform.portrait.data
            extension = image.filename.split(".")[-1]

            if request.form["source"] == "summary":
                # get char_id and check against filename sans extension
                # add new file using char_id as file name while preserving file format
                # May have to change in the future because O(n) could get expensive on a server
                for root, dirs, files in os.walk(
                    os.path.join(current_app.root_path, r"static\assets\uploaded-img")
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
                        current_app.root_path,
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
                    os.path.join(current_app.root_path, r"static\assets\uploaded-img")
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
                        current_app.root_path,
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


@card_maker.route("/character")
def retrieve_char_details():
    """Get all details of char from booth XIVAPI/Lodestone and FFLogs"""
    portraitform = UploadPortraitForm()
    bsform = BusinessImages()

    hookform = RPHookForm()
    traitform = RPTraitsForm()
    charsummaryform = RPCharSummary()
    nicknamesform = RPCharAlias()
    charquoteform = RPCharQuote()
    rpsocialsform = RPOOCSocials()
    rpaboutmeform = RPOOCAboutMe()

    venuenameform = VenueNameAndTagline()
    venuecontactform = VenueContactAndSocials()
    venuestaffform = VenueStaffDetails()

    try:
        # Character's lodestone id
        lodestone_id = int(request.args.get("charid"))
        portraitform.char_id_summary.data = lodestone_id
        bsform.char_id_bs.data = lodestone_id
        src = {}

        # TODO change to saving paths/links in database
        for root, dirs, files in os.walk(
            os.path.join(current_app.root_path, r"static\assets\uploaded-img")
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
                    print(rf"{root}\{splitted[0]}{splitted[1]}")
                    src["roleplay"] = url_for(
                        "static", filename=f"/assets/uploaded-img/{name}"
                    )
                elif splitted[0] == str(portraitform.char_id_summary.data)+"_venue_1":
                    print("one of two")
                    print(rf"{root}\{splitted[0]}{splitted[1]}")
                    src["one"] = url_for(
                        "static", filename=f"/assets/uploaded-img/{name}"
                    )
                elif splitted[0] == str(portraitform.char_id_summary.data)+"_venue_2":
                    print("two of two")
                    print(rf"{root}\{splitted[0]}{splitted[1]}")
                    src["two"] = url_for(
                        "static", filename=f"/assets/uploaded-img/{name}"
                    )
                elif splitted[0] == str(portraitform.char_id_summary.data)+"_venue_big":
                    print("big")
                    print(rf"{root}\{splitted[0]}{splitted[1]}")
                    src["big"] = url_for(
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
        retrieved_database = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id == lodestone_id)).scalar()
    except TypeError as error:
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
        # condition check edit mode or no
        mode = request.args.get("mode", None)
        if mode == "edit":
            return render_template(
                "card.html",
                character=retrieved_data.to_dict(),
                raid=retrieved_logs.to_dict()
                if retrieved_logs is not None
                else None,
                collectible=retrieve_collectibles,
                database=retrieved_database,
                form=portraitform,
                bsform=bsform,
                hookform=hookform,
                traitform=traitform,
                charsummaryform=charsummaryform,
                nicknamesform=nicknamesform,
                charquoteform=charquoteform,
                rpsocialsform=rpsocialsform,
                rpaboutmeform=rpaboutmeform,
                venuenameform=venuenameform,
                venuecontactform=venuecontactform,
                venuestaffform=venuestaffform,
                src=src,
                is_edit=True,
            )
        elif mode == "view" or mode is None:
            return render_template(
                "card.html",
                character=retrieved_data.to_dict(),
                raid=retrieved_logs.to_dict()
                if retrieved_logs is not None
                else None,
                collectible=retrieve_collectibles,
                database=retrieved_database,
                src=src,
                is_edit=False,
            )
    return render_template("card.html")

@card_maker.route("/char-summary", methods=["POST"])
def save_char_summary():
    """Saves the Char Summary section of a Character's page."""

    if request.method == "POST":
        retrieved = request.get_json()
        get_char = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==retrieved["char_id"])).scalar()
        get_char.summary = request.get_json()["summary"]
        db.session.commit()
        return jsonify({"summary": get_char.summary})
    

@card_maker.route("/rp-alias", methods=["GET", "POST"])
def save_roleplaying_alias():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==char_id)).scalar()
    if request.method == "POST":
        data = RPCharAlias()
        if data.validate():
            char_rp = check_roleplaying(get_char)
            char_rp.alias = data.alias.data
            db.session.commit()
            return jsonify({"status":"ok", "alias": char_rp.alias})
        else:
            return jsonify({"status":"error", "errors": data.errors})
    else:
        return jsonify({"status":"ok", "alias": get_char.roleplaying.alias})

@card_maker.route("/rp-summary", methods=["GET", "POST"])
def save_roleplaying_summary():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPCharSummary()
        if data.validate():
            try:
                char_rp = check_roleplaying(get_char)
                char_rp.age = data.age.data
                char_rp.gender = data.gender.data
                char_rp.sexuality = data.sexuality.data
                char_rp.relationship_status = data.relationship.data
                db.session.commit()
            # TODO server-side error exception handling, respond with error code
            except Exception as e:
                return jsonify({"status": "server-error", "msg": str(e)})
            else:
                return jsonify({
                    "status": "ok",
                    "age": char_rp.age,
                    "gender": char_rp.gender,
                    "sexuality": char_rp.sexuality,
                    "relationship": char_rp.relationship_status
                })
        else:
            return jsonify({"status":"error","errors":data.errors})
    else:
        return jsonify({
            "status": "ok",
            "age": get_char.roleplaying.age,
            "gender": get_char.roleplaying.gender,
            "sexuality": get_char.roleplaying.sexuality,
            "relationship": get_char.roleplaying.relationship_status
        })
    
@card_maker.route("/rp-socials", methods=["GET", "POST"])
def save_roleplaying_socials():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPOOCSocials()
        if data.validate():
            try:
                char_rp = check_roleplaying(get_char)
                char_rp.twitter = data.twitter.data
                char_rp.website = data.website.data
                char_rp.discord = data.discord.data
                char_rp.oc_notes = data.oc_notes.data
                db.session.commit()
            except Exception as e:
                return jsonify({"status": "server-error", "msg": str(e)})
            else:
                return jsonify({
                    "status": "ok",
                    "twitter": char_rp.twitter,
                    "website": char_rp.website,
                    "discord": char_rp.discord,
                    "oc_notes": char_rp.oc_notes
                })
        else:
            return jsonify({"status":"error","errors":data.errors})
    else:
        return jsonify({
            "status": "ok",
            "twitter": get_char.roleplaying.twitter,
            "website": get_char.roleplaying.website,
            "discord": get_char.roleplaying.discord,
            "oc_notes": get_char.roleplaying.oc_notes
        })


@card_maker.route("/rp-venue-mode", methods=["POST"])
def swtich_rp_venue():
    print(request.method)
    if request.method == "POST":
        print(request.get_json()["state"])
        data = request.get_json()
        char_id = data["char_id"]
        get_char = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==char_id)).scalar()
        get_char.is_business = data["state"]
        db.session.commit()
        return jsonify({"state": get_char.is_business})


def check_roleplaying(character: PlayerCharacter) -> Roleplaying:
    """Checks if a Roleplaying child exists within a PlayerCharacter
        :param character: A PlayerCharacter model
        :rtype: Roleplaying
        :return: The PlayerCharacter associated Roleplaying model
    """
    if character.roleplaying:
        return character.roleplaying
    else:
        character.roleplaying = Roleplaying()
        return character.roleplaying


def retrieve_char_id_from_ajax(req: request) -> int:
    """Retrieves the Char ID from an AJAX POST Request Body or URI Args
        :param req: The request data
        :rtype: int
        :return: The char_id as an integer
    """
    return request.form.get("char_id") if request.form.get("char_id") is not None else request.args.get("char_id")


def retrieve_char_by_char_id(char_id: int) -> PlayerCharacter:
    """Retrieves the PlayerCharacter using the char_id, returns the object if it exists, else it returns None

        :param char_id: The char_id of a PlayerCharacter
        :rtype: PlayerCharacter
        :return: The PlayerCharacter associated with the char_id
    """
    return db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==char_id)).scalar()
