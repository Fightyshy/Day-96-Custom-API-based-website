from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
    url_for,
)
from .api_fetchers import (
    get_collectibles,
    get_fflogs_token,
    get_fflogs_character,
    get_lodestone_char_basic,
    merge_raids
)
import os
from werkzeug.utils import secure_filename

from ..objects.forms import (
    BusinessImages,
    RPCharNicknames,
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

card_maker = Blueprint("card_maker", __name__, templates="templates")

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


@card_maker.route("/character/portrait", methods=["POST"])
def upload_portrait():
    if request.method == "POST":
        portraitform = UploadPortraitForm()
        if portraitform.validate():
            image = portraitform.portrait.data
            extension = image.filename.split(".")[-1]

            if request.form["source"] == "summary":
                # TODO get char_id and check against filename sans extension
                # TODO add new file using char_id as file name while preserving file format
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
    nicknamesform = RPCharNicknames()
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
                aliases="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
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
