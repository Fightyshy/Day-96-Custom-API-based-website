from itertools import groupby
import json
import os
from flask import url_for
import requests
from requests.auth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from gql import Client
from gql.dsl import DSLQuery, DSLSchema, dsl_gql
from gql.transport.requests import RequestsHTTPTransport
from character import Character, CharacterRaids
from const_loader import CharacterData, MetaLinks, Raidzones, Servers
from dotenv import load_dotenv
import bs4
from flask_caching import Cache

cache = Cache()

load_dotenv()

#fflogs consts
CLIENT_KEY = os.environ.get("FFLOGS_KEY")
CLIENT_SECRET = os.environ.get("FFLOGS_SECRET")  # for private api
FFLOGS_API_URL = "https://www.fflogs.com/api/v2/client"
AUTHORIZE_URI = "https://www.fflogs.com/oauth/authorize"
TOKEN_URI = "https://www.fflogs.com/oauth/token"

# Consts
# Name | DC | Region
SERVERS = Servers()
RAIDS = Raidzones()
META_LINKS = MetaLinks()
CHARACTER_SELECTORS = CharacterData()

# xivapi consts and globals
# PRIVATE_KEY = os.environ["XIVAPI_PRIVATE"]
# XIVAPI_CHAR_URL = "https://xivapi.com/character/"

FFXIV_COLLECT = "https://ffxivcollect.com/api/characters/%i"
FFXIV_COLLECT_EXTERNALS = "/%s/%s"

# fixed number counts



# XIVAPI request funcs
@cache.memoize(timeout=3600)
def get_lodestone_char_basic(char_id: int) -> Character:
    """Retrieve basic character data for AP summary/front plate. Lodestone data scrapeed via BS, as XIVApi endpoints are broken currently."""

    # Soups scrape and parse
    char_summary_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/character.json"] % ("na", char_id))
    char_summary_response.raise_for_status()
    char_summary_soup = bs4.BeautifulSoup(char_summary_response.text, "html.parser")

    char_classjob_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/classjob.json"] % ("na", char_id))
    char_classjob_response.raise_for_status()
    char_classjob_soup = bs4.BeautifulSoup(char_classjob_response.text, "html.parser")

    freecompany_id = char_summary_soup.select_one(CHARACTER_SELECTORS.character["FREE_COMPANY"]["ID"]["selector"])
    if freecompany_id is not None:
        char_free_company_response = requests.get(META_LINKS.meta_links["applicableUris"]["freecompany/freecompany.json"] % ("na", int(freecompany_id["href"].split("/")[-2]))) if freecompany_id is not None else None
        char_free_company_response.raise_for_status()
        char_free_company_soup = bs4.BeautifulSoup(char_free_company_response.text, "html.parser")
        # free company details
        freecompany = {
            "name": char_summary_soup.select_one(CHARACTER_SELECTORS.character["FREE_COMPANY"]["NAME"]["selector"]).text,
            "tag": char_free_company_soup.select_one(CHARACTER_SELECTORS.freecompany["TAG"]["selector"]).text,
            "top": char_free_company_soup.select_one(CHARACTER_SELECTORS.freecompany["CREST_LAYERS"]["TOP"]["selector"])["src"],
            "middle": char_free_company_soup.select_one(CHARACTER_SELECTORS.freecompany["CREST_LAYERS"]["MIDDLE"]["selector"])["src"],
            "bottom": char_free_company_soup.select_one(CHARACTER_SELECTORS.freecompany["CREST_LAYERS"]["BOTTOM"]["selector"])["src"],
        }
    else:
        freecompany = None

    # pre-processing
    # clean and split server
    dcserver = char_summary_soup.select_one(CHARACTER_SELECTORS.character["SERVER"]["selector"]).text.split()
    dcserver[1] = dcserver[1][1:len(dcserver[1])-1]

    title = char_summary_soup.select_one(CHARACTER_SELECTORS.character.get("TITLE")["selector"])

    race_gender = char_summary_soup.select_one(CHARACTER_SELECTORS.character["RACE_CLAN_GENDER"]["selector"]).text.split(" / ")
    # TODO get achieves and mount/minion data for that page
    found_char = Character(name=char_summary_soup.select_one(CHARACTER_SELECTORS.character["NAME"]["selector"]).text,
                           dcserver=dcserver,
                           title=title.text if title is not None else None,
                           race={
                            #    https://stackoverflow.com/a/58083736
                               "race":"".join([(" "+i if i.isupper() else i) for i in race_gender[0]]).strip().split(),
                               "gender":race_gender[1]
                           },
                           nameday=char_summary_soup.select_one(CHARACTER_SELECTORS.character["NAMEDAY"]["selector"]).text,
                           twelve={
                               "name":char_summary_soup.select_one(CHARACTER_SELECTORS.character["GUARDIAN_DEITY"]["NAME"]["selector"]).text,
                               "icon":char_summary_soup.select_one(CHARACTER_SELECTORS.character["GUARDIAN_DEITY"]["ICON"]["selector"]).attrs["src"]
                           },
                           char_jobs=scrape_and_format_jobs(char_classjob_soup),
                           freecompany=freecompany
                           )
    return found_char

# 0 is infinite cache
@cache.cached(timeout=0, key_prefix="ffxiv_cached_resources")
def ffxiv_cached_resources():
    print("executing cacher")
    cached_mounts = requests.get("https://ffxivcollect.com/api/mounts")
    cached_mounts.raise_for_status()
    cached_mounts = cached_mounts.json()
    cached_mounts = {mount["name"]: mount for mount in cached_mounts["results"]}

    cached_minions = requests.get("https://ffxivcollect.com/api/minions")
    cached_minions.raise_for_status()
    cached_minions = cached_minions.json()
    cached_minions = {minion["name"]: minion for minion in cached_minions["results"]}

    cached_achievements = requests.get("https://ffxivcollect.com/api/achievements")
    cached_achievements.raise_for_status()
    cached_achievements = cached_achievements.json()
    cached_achievements = {achieve["id"]: achieve for achieve in cached_achievements["results"]}
    return {
        "mounts":cached_mounts,
        "minions": cached_minions,
        "achievements": cached_achievements
    }

# @cache.memoize(timeout=100)
# def lodestone_achievement_scrape(char_id: int):
#     header = {
#         "User-Agent": META_LINKS.meta_links["userAgentMobile"]
#     }

#     char_mount_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/mount.json"] % ("na", char_id), headers=header)
#     char_mount_response.raise_for_status()
#     char_mount_soup = bs4.BeautifulSoup(char_mount_response.text, "html.parser")

#     char_minion_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/minion.json"] % ("na", char_id), headers=header)
#     char_minion_response.raise_for_status()
#     char_minion_soup = bs4.BeautifulSoup(char_minion_response.text, "html.parser")
#     test = [entry.text for entry in char_mount_soup.select(".mount__name")]
#     test2 = [entry.text for entry in char_minion_soup.select(".minion__name")]
#     print(test)
#     print(test2)
#     return test

# TODO bigo optimise, ~2000 data points at worst being retrieved.
# TODO there are ~68 categories to scrape
@cache.memoize(timeout=3600)
def get_collectibles(char_id: int) -> dict:
    """Gets mount, minion, and achivevements of character using the char_id"""
    # Bypass circular import restrictiion by importing on func execute
    from main import COLLECT_CACHE, LEN_MOUNTS, LEN_ACHIEVES, LEN_MINIONS

    # query ffxiv_collect once to build cache of objects
    # scrape and match id/names once only, timeout every x

    header = {
        "User-Agent": META_LINKS.meta_links["userAgentMobile"]
        }

    char_mount_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/mount.json"] % ("na", char_id), headers=header)
    char_mount_response.raise_for_status()
    char_mount_soup = bs4.BeautifulSoup(char_mount_response.text, "html.parser")

    char_minion_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/minion.json"] % ("na", char_id), headers=header)
    char_minion_response.raise_for_status()
    char_minion_soup = bs4.BeautifulSoup(char_minion_response.text, "html.parser")

    char_portrait_response = requests.get(META_LINKS.meta_links["applicableUris"]["profile/character.json"] % ("na", char_id))
    char_portrait_response.raise_for_status()
    char_portrait = bs4.BeautifulSoup(char_portrait_response.text, "html.parser")

    collected_mounts = [COLLECT_CACHE["mounts"][name.text] for name in char_mount_soup.select(CHARACTER_SELECTORS.mounts["MOUNTS"]["NAME"]["selector"])]
    collected_minions = [COLLECT_CACHE["minions"][name.text] for name in char_minion_soup.select(CHARACTER_SELECTORS.minions["MINIONS"]["NAME"]["selector"])]

    achieve_urls = [f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/1/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/2/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/3/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/4/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/5/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/8/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/11/#anchor_achievement",
            f"https://na.finalfantasyxiv.com/lodestone/character/{char_id}/achievement/kind/12/#anchor_achievement"]

    achieves = []
    for url in achieve_urls:
        requester = requests.get(url)
        requester.raise_for_status()
        requester = bs4.BeautifulSoup(requester.text, "html.parser")
        achieves += [entry.attrs["href"].split("/")[-2] for entry in requester.find_all("a", class_="entry__achievement--complete")]

    collected_achieves = [COLLECT_CACHE["achievements"][int(id)] for id in achieves]
    sortachieves = {}
    for entry in collected_achieves:
        _type = entry.get("type").get("name")
        _category = entry.get("category").get("name")
        if sortachieves.get(_type) is None:
            sortachieves[_type] = {}
        if sortachieves.get(_type).get(_category) is None:
            sortachieves[_type][_category] = []
        sortachieves[_type][_category].append(entry)
    # duplicate structure so no special template conditions required
    print(char_portrait.select_one(CHARACTER_SELECTORS.character["PORTRAIT"]["selector"]).attrs["src"])
    return {
        "character": {
            "portrait":char_portrait.select_one(CHARACTER_SELECTORS.character["PORTRAIT"]["selector"]).attrs["src"],
            "achievements":{
                "count": len(sortachieves),
                "total": LEN_ACHIEVES
            },
            "mounts":{
                "count": len(collected_mounts),
                "total": LEN_MOUNTS
            },
            "minions":{
                "count":len(collected_minions),
                "total": LEN_MINIONS
            }
        },
        "mounts": collected_mounts,
        "minions": collected_minions,
        "achievements": sortachieves
    }

    # else:
    #     owned_mounts = requests.get(owner_uri + FFXIV_COLLECT_EXTERNALS % ("mounts", "owned"),
    #                                 params={"latest": True})
    #     owned_mounts.raise_for_status()
    #     owned_minions = requests.get(owner_uri + FFXIV_COLLECT_EXTERNALS % ("minions", "owned"),
    #                                 params={"latest": True})
    #     owned_minions.raise_for_status()
    #     owned_achieves = requests.get(owner_uri + FFXIV_COLLECT_EXTERNALS % ("achievements", "owned"),
    #                                 params={"latest": True})
    #     owned_achieves.raise_for_status()

    #     # grouping by
    #     # type > categories > achievement
    #     sortachieves = {}
    #     for entry in owned_achieves.json():
    #         _type = entry.get("type").get("name")
    #         _category = entry.get("category").get("name")
    #         if sortachieves.get(_type) is None:
    #             sortachieves[_type] = {}
    #         if sortachieves.get(_type).get(_category) is None:
    #             sortachieves[_type][_category] = []
    #         sortachieves[_type][_category].append(entry)

    #     return {
    #         "character": owner.json(),
    #         "mounts": owned_mounts.json(),
    #         "minions": owned_minions.json(),
    #         "achievements": sortachieves
    #     }

# FFLogs request funcs
@cache.cached(timeout=3600, key_prefix="fflogs_token")
def get_fflogs_token() -> dict:
    """Returns a new auth bearer token from fflogs as a dict ready to be used in a header"""

    # token_params = {
    #     "client_id":CLIENT_KEY,
    #     "code_challenge":hashed,
    #     "code_challenge_method": "S256",
    #     "state":"",
    #     "redirect_uri":AUTHORIZE_URI,
    #     "response_type": 200
    # }

    # Only public data with this method
    response = requests.post(TOKEN_URI, auth=HTTPBasicAuth(CLIENT_KEY,CLIENT_SECRET), data={"grant_type":"client_credentials"})
    response.raise_for_status()
    print("Token recived")
    return {"Authorization":f"Bearer {response.json()["access_token"]}"}

@cache.memoize(timeout=3600)
# TODO savage+ stats only, currently gets normal parse if it exists as well
def get_fflogs_character(token:dict, name:str, server:str, region:str)->dict:
    #Form GraphQL query, structure each curly is a query layer deeper, accessed vars inside deepest query
    # Zone is tier
    # Encounter is fight
    # therefore each savage zone is 4-5 encounters (5th is a boss' checkpointed second phase if applicable)
    # Ultimates are different, as they have a "current content" zone and "legacy" zone
    # Each current content zone has one encounter - the ultimate raid of the patch
    # Each legacy zone has all the previous ultimate raids before the expac 

    # we are running synced, i.e. everything executes sequentially on command
    # so we use RequestHTTPTransport method
    trans = RequestsHTTPTransport(
        url=FFLOGS_API_URL,
        verify=True,
        headers=token
    )

    # inst GraphQL client using aiohttp transport
    client = Client(transport=trans, fetch_schema_from_transport=True)

    # Open connection session using client
    with client as session:
        # Check if we successfully get schema from graphql server
        assert client.schema is not None
        # Inst schema domain specific language schema obj
        ds = DSLSchema(client.schema)

        #build query
        query = dsl_gql(
            DSLQuery(
                # start query and select obj by name
                ds.Query.characterData.select(
                    # second select for nested obj by name, with where==value param
                    ds.CharacterData.character(name=name, serverSlug=server, serverRegion=region).select(
                        # fields to get
                        ds.Character.name,  # counter-check against xivapi data

                        # savages
                        ew1=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Asphodelos"),difficulty=101),  # we sort by zones performance, set alias
                        ew2=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Abyssos"),difficulty=101), # also force savage-only values
                        ew3=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Anabaseios"),difficulty=101),

                        shb1=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Eden's Gate"),difficulty=101),
                        shb2=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Eden's Verse"),difficulty=101),
                        shb3=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Eden's Promise"),difficulty=101),

                        # difficulty was only selectable from shb onwards
                        sb1=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Deltascape")),
                        sb2=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Sigmascape")),
                        sb3=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Alphascape")),

                        hw1=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Alexander: Gordias")),
                        hw2=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Alexander: Midas")),
                        hw3=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Alexander: The Creator")),

                        # Ults
                        top=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("The Omega Protocol")), # no difficulty forced, the only difficulty in ultimates is pain
                        dsr=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Dragonsong's Reprise")),
                        legacy_ults=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Legacy ultimates (Endwalker)")),
                        shbtea=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("The Epic of Alexander (Shadowbringers)")),
                        sbinshb=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Legacy ultimates (Shadowbringers)")),
                        sbuwu=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("The Weapon's Refrain (Stormblood)")),
                        sbucob=ds.Character.zoneRankings(zoneID=RAIDS.tier_to_ids("Unbinding Coil of Bahamut (Stormblood)")),
                    )
                )
            )
        )

        # execute query and return
        result = session.execute(query)
        print(result)
        return result

# Helper funcs

def scrape_and_format_jobs(classjob_soup:bs4.BeautifulSoup)->list:
    jobs = []
    for key in CHARACTER_SELECTORS.classjob:
        if (key == "BOZJA") or (key == "EUREKA"):
            pass
        else:
            name=classjob_soup.select_one(CHARACTER_SELECTORS.classjob[key]["UNLOCKSTATE"]["selector"]).text
            level = classjob_soup.select_one(CHARACTER_SELECTORS.classjob[key]["LEVEL"]["selector"]).text
            abbr = CHARACTER_SELECTORS.abbreviation.get(name)
            jobs.append({
                "name":name,
                "level":level,
                "abbrevation":abbr,
                "role":CHARACTER_SELECTORS.role.get(name),
                "icon_local":url_for('static', filename=f"assets/job_icons/{secure_filename(name.lower())}.png")
            })
    return jobs


def merge_raids(raidlogs:dict)->CharacterRaids:
    if raidlogs["characterData"]["character"] is None:
        return None
    else:
        logs = raidlogs["characterData"]["character"]
        ew = {
            "anabaseios":logs["ew3"],
            "abyssos":logs["ew2"],
            "asphodelos":logs["ew1"],
        }
        shb = {
            "eden's promise":logs["shb3"],
            "eden's verse":logs["shb2"],
            "eden's gate":logs["shb1"],
        }
        sb = {
            "alphascape":logs["sb3"],
            "sigmascape":logs["sb2"],
            "deltascape":logs["sb1"],
        }
        hw = {
            "alexander: the creator":logs["hw3"],
            "alexander: midas":logs["hw2"],
            "alexander: gordias":logs["hw1"],
        }
        ults = {
            "the omega protocol":logs["top"],
            "dragonsong's reprise":logs["dsr"],
            "legacy ultimates (endwalker)":logs["legacy_ults"],
            "the epic of alexander (shadowbringers)": logs["shbtea"],
            "legacy ultimates (shadowbringers)": logs["sbinshb"],
            "the weapon's refrain (stormblood)": logs["sbuwu"],
            "unbinding coil of bahamut (stormblood)": logs["sbucob"]
        }

        return CharacterRaids(endwalker=ew, shadowbringers=shb, stormblood=sb, heavensward=hw, ultimates=ults)
