from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    url_for,
)
from sqlalchemy import and_
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
from ..models.models import Business, Hook, PlayerCharacter, Roleplaying, Trait, VenueAddress, VenueStaff, db
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


@card_maker.route("/rp-about-me", methods=["GET", "POST"])
def save_roleplaying_about_me():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPOOCAboutMe()
        if data.validate():
            try:
                char_rp = check_roleplaying(get_char)
                char_rp.about_me = data.about_me.data
                db.session.commit()
            except Exception as e:
                return jsonify({"status": "server-error", "msg": str(e)})
            else:
                return jsonify({
                    "status": "ok",
                    "about_me": char_rp.about_me
                })
        else:
            return jsonify({"status":"error","errors":data.errors})
    else:
        return jsonify({
            "status": "ok",
            "about_me": get_char.roleplaying.about_me
        })


@card_maker.route("/rp-char-quote", methods=["GET", "POST"])
def save_roleplaying_quote():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPCharQuote()
        if data.validate():
            try:
                char_rp = check_roleplaying(get_char)
                char_rp.tagline = data.quote.data
                db.session.commit()
            except Exception as e:
                return jsonify({"status": "server-error", "msg": str(e)})
            else:
                return jsonify({
                    "status": "ok",
                    "quote": char_rp.tagline
                })
        else:
            return jsonify({"status":"error","errors":data.errors})
    else:
        return jsonify({
            "status": "ok",
            "quote": get_char.roleplaying.tagline
        })


@card_maker.route("/rp-hooks", methods=["GET", "POST"])
def save_roleplaying_hooks():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPHookForm()
        if data.validate():
            # variable setup, get roleplaying, hooks, and sanitised data_dict from data
            char_rp = check_roleplaying(get_char)
            data_dict = data.data
            data_dict.pop("submit_hooks")
            data_dict.pop("csrf_token")

            # init response dict
            response = {"status": "ok"}

            # setup loop that does 3 iterations, for the 3 hooks per char
            for i in range(3):
                # check if data exists
                current_hook_title = data_dict.get(f"hook{i+1}_title")
                retrieved_hook = db.session.execute(db.select(Hook)
                                                    .where(and_(Hook.number==i+1, Hook.roleplaying==char_rp))).scalar()
                # if both exist (len data_dict>=1, retrieved_hook is not None), update it
                if retrieved_hook and len(current_hook_title) >= 1:
                    retrieved_hook.title = data_dict.get(f"hook{i+1}_title")
                    retrieved_hook.body = data_dict.get(f"hook{i+1}_body")
                    db.session.commit()
                    response[f"hook{i+1}_title"] = retrieved_hook.title
                    response[f"hook{i+1}_body"] = retrieved_hook.body
                # if it's not in the db but it's in the data_dict (new entry), add it
                elif not retrieved_hook and len(current_hook_title) >= 1:
                    new_hook = Hook(title=current_hook_title,
                                    body=data_dict.get(f"hook{i+1}_body"),
                                    number=i+1,
                                    roleplaying=char_rp)
                    db.session.add(new_hook)
                    db.session.commit()
                    response[f"hook{i+1}_title"] = new_hook.title
                    response[f"hook{i+1}_body"] = new_hook.body
                # if it's in the db but doesn't exst in data_dict, (was removed), delete it
                elif current_hook_title == "" and retrieved_hook:
                    db.session.delete(retrieved_hook)
                    db.session.commit()

            return jsonify(response)
        else:
            return jsonify({"status": "error", "errors": data.errors})
    else:
        # TODO if hook is empty respond with defaults
        hooks = {"status": "ok"}
        for hook in get_char.roleplaying.hooks:
            hooks[f"hook{hook.number}_title"] = hook.title
            hooks[f"hook{hook.number}_body"] = hook.body
        return jsonify(hooks)


@card_maker.route("/rp-traits", methods=["GET", "POST"])
def save_roleplaying_traits():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)
    if request.method == "POST":
        data = RPTraitsForm(request.form)
        if data.validate():
            char_rp = check_roleplaying(get_char)
            data_dict = data.data
            data_dict.pop("submit_traits")
            data_dict.pop("csrf_token")

            response = {"status": "ok"}

            # loop 5 times, we use 2 pointers to get pos and neg traits
            for i in range(5):
                # loop both types simultaenously
                current_pos_trait = data_dict.get(f"pos_trait{i+1}")
                current_neg_trait = data_dict.get(f"neg_trait{i+1}")

                # get both at the same time as well, 10 queries worst case
                retrieved_pos_trait = db.session.execute(
                    db.select(Trait).where(and_(Trait.number == i+1,
                                                Trait.roleplaying == char_rp,
                                                Trait.type == "pos"))).scalar()
                retrieved_neg_trait = db.session.execute(
                    db.select(Trait).where(and_(Trait.number == i+1,
                                                Trait.roleplaying == char_rp,
                                                Trait.type == "neg"))).scalar()

                # Works for now, separate ifs, same function for each
                # Also 10 queries worst case
                if retrieved_pos_trait and len(current_pos_trait) >= 1:
                    retrieved_pos_trait.trait = current_pos_trait
                    db.session.commit()
                    response[f"pos_trait{i+1}"] = retrieved_pos_trait.trait
                elif not retrieved_pos_trait and len(current_pos_trait) >= 1:
                    new_trait = Trait(number=i+1,
                                      type="pos",
                                      trait=current_pos_trait,
                                      roleplaying=char_rp)
                    db.session.add(new_trait)
                    db.session.commit()
                    response[f"pos_trait{i+1}"] = new_trait.trait
                elif current_pos_trait == "" and retrieved_pos_trait:
                    db.session.delete(retrieved_pos_trait)
                    db.session.commit()

                if retrieved_neg_trait and len(current_neg_trait) >= 1:
                    retrieved_neg_trait.trait = current_neg_trait
                    db.session.commit()
                    response[f"neg_trait{i+1}"] = retrieved_neg_trait.trait
                elif not retrieved_neg_trait and len(current_neg_trait) >= 1:
                    new_trait = Trait(number=i+1,
                                      type="neg",
                                      trait=current_neg_trait,
                                      roleplaying=char_rp)
                    db.session.add(new_trait)
                    db.session.commit()
                    response[f"neg_trait{i+1}"] = new_trait.trait
                elif current_neg_trait == "" and retrieved_neg_trait:
                    db.session.delete(retrieved_neg_trait)
                    db.session.commit()
            # 20 queries at worst
            return jsonify(response)
        else:
            return jsonify({"status": "error", "errors": data.errors})
    else:
        traits = {"status": "ok"}
        for trait in get_char.roleplaying.traits:
            traits[f"{trait.type}_trait{trait.number}"] = trait.trait
        return jsonify(traits)


@card_maker.route("/rp-venue-names", methods=["GET", "POST"])
def save_venue_names():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)

    if request.method == "POST":
        data = VenueNameAndTagline()
        if data.validate():
            char_business = check_business(get_char)
            char_business.venue_name = data.venue_name.data
            char_business.venue_tagline = data.venue_tagline.data
            db.session.commit()
            return jsonify({"status":"ok",
                            "venue_name":char_business.venue_name,
                            "venue_tagline":char_business.venue_tagline})
        else:
            return jsonify({
                "status": "error",
                "errors": data.errors
            })
    else:
        return jsonify({
            "status": "ok",
            "venue_name": get_char.business.venue_name,
            "venue_tagline": get_char.business.venue_tagline
        })


@card_maker.route("/rp-venue-staff", methods=["GET", "POST"])
def save_venue_staff_details():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)

    if request.method == "POST":
        data = VenueStaffDetails()
        if data.validate():
            char_business = check_business(get_char)
            if char_business.venue_staff:
                char_business.venue_staff.staff_role = data.staff_role.data
                char_business.venue_staff.staff_discord = data.staff_discord.data
                char_business.venue_staff.staff_twitter = data.staff_twitter.data
                char_business.venue_staff.staff_website = data.staff_website.data
            else:
                new_staff = VenueStaff(staff_role=data.staff_role.data,
                                       staff_discord=data.staff_discord.data,
                                       staff_twitter=data.staff_twitter.data,
                                       staff_website=data.staff_website.data,
                                       business=char_business)
                db.session.add(new_staff)
            db.session.commit()
            return jsonify({
                "status": "ok",
                "staff_role": get_char.business.venue_staff.staff_role,
                "staff_discord": get_char.business.venue_staff.staff_discord,
                "staff_twitter": get_char.business.venue_staff.staff_twitter,
                "staff_website": get_char.business.venue_staff.staff_website
            })
        else:
            return jsonify({
                "status": "error",
                "errors": data.errors
            })
    else:
        return jsonify({
            "status": "ok",
            "staff_role": get_char.business.venue_staff.staff_role,
            "staff_discord": get_char.business.venue_staff.staff_discord,
            "staff_twitter": get_char.business.venue_staff.staff_twitter,
            "staff_website": get_char.business.venue_staff.staff_website
        })


@card_maker.route("/rp-venue-contacts", methods=["GET", "POST"])
def save_business_contacts():
    char_id = retrieve_char_id_from_ajax(request)
    get_char = retrieve_char_by_char_id(char_id)

    if request.method == "POST":
        data = VenueContactAndSocials()
        if data.validate():
            char_business = check_business(get_char)
            
            # preload data into char_business first
            char_business.venue_website = data.venue_website.data
            char_business.venue_operating_times = data.venue_operating_times.data
            char_business.venue_discord = data.venue_discord.data
            char_business.venue_twitter = data.venue_twitter.data

            # check if address model exists
            # address it 5 fields depending on what type of house it is
            if char_business.venue_address:
                # set housing zone/ward/housing type/server first
                char_business.venue_address.housing_zone = data.housing_zone.data
                char_business.venue_address.housing_ward = data.housing_ward.data
                char_business.venue_address.is_apartment = data.is_apartment.data
                char_business.venue_address.server = data.server.data
                char_business.venue_address.data_center = SERVERS.get_server_data_center(data.server.data)

                response = {
                    "status": "ok",
                    "housing_zone": char_business.venue_address.housing_zone,
                    "housing_ward": char_business.venue_address.housing_ward,
                    "server": char_business.venue_address.server,
                    "data_center": char_business.venue_address.data_center,
                    "venue_website": char_business.venue_website,
                    "venue_operating_times": char_business.venue_operating_times,
                    "venue_discord": char_business.venue_discord,
                    "venue_twitter": char_business.venue_twitter
                }
                # check if apartment or house plot, save one and delete the other
                if data.is_apartment.data:
                    char_business.venue_address.apartment_num = data.apartment_num.data
                    char_business.venue_address.ward_plot = 0
                    response["apartment_num"] = char_business.venue_address.apartment_num
                else:
                    char_business.venue_address.ward_plot = data.ward_plot.data
                    char_business.venue_address.apartment_num = 0
                    response["ward_plot"] = char_business.venue_address.ward_plot
                db.session.commit()
                return jsonify(response)
            else:
                new_address = VenueAddress()
                new_address.housing_zone = data.housing_zone.data
                new_address.housing_ward = data.housing_ward.data
                new_address.is_apartment = data.is_apartment.data
                new_address.server = data.server.data
                new_address.data_center = SERVERS.get_server_data_center(data.server.data)
                new_address.business = char_business

                response = {
                    "status": "ok",
                    "housing_zone": new_address.housing_zone,
                    "housing_ward": new_address.housing_ward,
                    "server": new_address.server,
                    "data_center": new_address.data_center,
                    "venue_website": char_business.venue_website,
                    "venue_operating_times": char_business.venue_operating_times,
                    "venue_discord": char_business.venue_discord,
                    "venue_twitter": char_business.venue_twitter
                }

                if data.is_apartment.data:
                    new_address.apartment_num = data.apartment_num.data
                    response["apartment_num"] = new_address.apartment_num
                else:
                    new_address.ward_plot = data.ward_plot.data
                    response["ward_plot"] = new_address.ward_plot
                db.session.add(new_address)
                db.session.commit()
                return jsonify(response)
        else:
            return jsonify({"status":"error","errors":data.errors})
    else:
        if get_char.business:
            response = {
                "status": "ok",
                "venue_website": get_char.business.venue_website,
                "venue_operating_times": get_char.business.venue_operating_times,
                "venue_discord": get_char.business.venue_discord,
                "venue_twitter": get_char.business.venue_twitter,
                "is_apartment": get_char.business.venue_address.is_apartment,
                "housing_zone": get_char.business.venue_address.housing_zone,
                "housing_ward": get_char.business.venue_address.housing_ward,
                "server": get_char.business.venue_address.server
            }
            if get_char.business.venue_address:
                if get_char.business.venue_address.is_apartment:
                    response["apartment_num"] = get_char.business.venue_address.apartment_num
                else:
                    response["ward_plot"] = get_char.business.venue_address.ward_plot
            return jsonify(response)
        else:
            return jsonify({
                "status": "empty",
                "is_apartment": False
            })


@card_maker.route("/rp-venue-mode", methods=["POST"])
def swtich_rp_venue():
    if request.method == "POST":
        data = request.get_json()
        char_id = data["char_id"]
        get_char = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id==char_id)).scalar()
        get_char.is_business = data["state"]
        db.session.commit()
        return jsonify({"state": get_char.is_business})

# TODO fix roleplay check to return None if None
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


def check_business(character: PlayerCharacter) -> Business:
    """Checks if a Business child exists within a PlayerCharacter
        :param character: A PlayerCharacter model
        :rtype: Business
        :return: The PlayerCharacter associated Business model
    """
    if character.business:
        return character.business
    else:
        character.business = Business()
        return character.business


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
