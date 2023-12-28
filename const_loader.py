import csv
import json


class Servers:
    def __init__(self) -> None:
        self.jp_servers = self.get_jp()
        self.na_servers = self.get_NA()
        self.eu_servers = self.get_EU()
        self.oc_servers = self.get_OC()

    # TODO code optimisation
    def get_region(self, server: str) -> str:
        for servers in self.jp_servers:
            if servers["server-name"] == server:
                return servers["server-region"]
        for servers in self.na_servers:
            if servers["server-name"] == server:
                return servers["server-region"]
        for server in self.eu_servers:
            if servers["server-name"] == server:
                return servers["server-region"]
        for servers in self.oc_servers:
            if servers["server-name"] == server:
                return servers["server-region"]

    def get_jp(self) -> list:
        server = []
        with open(
            r"static/assets/constants/server_region_JP.csv"
        ) as jpservers:
            file = csv.DictReader(jpservers)
            for row in file:
                server.append(
                    {
                        "server-name": row["server-name"],
                        "server-dc": row["server-dc"],
                        "server-region": row["server-region"],
                    }
                )
        return server

    def get_NA(self) -> list:
        server = []
        with open(
            r"static/assets/constants/server_region_NA.csv"
        ) as jpservers:
            file = csv.DictReader(jpservers)
            for row in file:
                server.append(
                    {
                        "server-name": row["server-name"],
                        "server-dc": row["server-dc"],
                        "server-region": row["server-region"],
                    }
                )
        return server

    def get_EU(self) -> list:
        server = []
        with open(
            r"static/assets/constants/server_region_EU.csv"
        ) as jpservers:
            file = csv.DictReader(jpservers)
            for row in file:
                server.append(
                    {
                        "server-name": row["server-name"],
                        "server-dc": row["server-dc"],
                        "server-region": row["server-region"],
                    }
                )
        return server

    def get_OC(self) -> list:
        server = []
        with open(
            r"static/assets/constants/server_region_OC.csv"
        ) as jpservers:
            file = csv.DictReader(jpservers)
            for row in file:
                server.append(
                    {
                        "server-name": row["server-name"],
                        "server-dc": row["server-dc"],
                        "server-region": row["server-region"],
                    }
                )
        return server


class Raidzones:
    def __init__(self) -> None:
        self.raidzones = self.get_zones()

    def get_zones(self):
        with open(r"static/assets/constants/raidzone_ids.csv") as raidzones:
            zones = [
                {
                    "tier": zone["tier"],
                    "expac": zone["expac"],
                    "id": zone["id"],
                }
                for zone in csv.DictReader(raidzones)
            ]
        return zones

    def tier_to_ids(self, tier: str) -> int:
        return next(
            (
                id["id"]
                for id in self.raidzones
                if tier.lower() == id["tier"].lower()
            ),
            None,
        )

    # TODO get list of expac tiers/ids for use
    def get_expac_raids(self, expac: str) -> list:
        return [tier for tier in self.raidzones if tier[expac.title()]]


class MetaLinks:
    def __init__(self) -> None:
        self.meta_links = self.get_meta_links()

    def get_meta_links(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\meta.json"
        ) as meta:
            return json.load(meta)


class CharacterData:
    def __init__(self) -> None:
        self.character = self.get_character_selectors()
        self.classjob = self.get_classjob_selectors()
        self.abbreviation = self.get_classjob_abbreviation()
        self.role = self.get_classjob_role()
        self.minions = self.get_minions()
        self.mounts = self.get_mounts()
        self.freecompany = self.get_freecompany()

    def get_character_selectors(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\profile\character.json"
        ) as chardata:
            return json.load(chardata)

    def get_classjob_selectors(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\profile\classjob.json"
        ) as chardata:
            return json.load(chardata)

    def get_classjob_abbreviation(self):
        with open(
            r"static\assets\constants\class_abbreviation.csv"
        ) as abbreviations:
            file = csv.DictReader(abbreviations)
            return {key["full"]: key["abbr"] for key in file}

    def get_classjob_role(sefl):
        with open(r"static\assets\constants\class_abbreviation.csv") as roles:
            file = csv.DictReader(roles)
            return {key["full"]: key["role"] for key in file}

    def get_minions(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\profile\minion.json"
        ) as minion:
            return json.load(minion)

    def get_mounts(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\profile\mount.json"
        ) as mount:
            return json.load(mount)

    def get_freecompany(self):
        with open(
            r"static\assets\lodestone-css-selectors-main\freecompany\freecompany.json"
        ) as freecompany:
            return json.load(freecompany)
