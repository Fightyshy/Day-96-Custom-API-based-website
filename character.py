# from character import CharacterRaids
from __future__ import annotations  # enable


class Character:
    def __init__(
        self,
        name: str,
        title: str,
        dcserver: str,
        race: str,
        nameday: str,
        twelve: str,
        char_jobs: dict,
        # mount_total: int,
        # minion_total: int,
        freecompany: dict,
        # char_raids: type[CharacterRaids] = None,
    ):
        self.name = name
        self.title = title
        self.dcserver = dcserver
        self.race = race
        self.nameday = nameday
        self.twelve = twelve
        self.char_jobs = char_jobs
        # self.char_raids = char_raids
        # self.mount_total = mount_total
        # self.minion_total = minion_total
        self.freecompany = freecompany

    # Manually formed, less pain
    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "dcserver": self.dcserver,
            "race": self.race,
            "nameday": self.nameday,
            "twelve": self.twelve,
            "char_jobs": self.char_jobs,
            # "char_raids": self.char_raids.to_dict(),
            # "mount_total": self.mount_total,
            # "minion_total": self.minion_total,
            "freecompany": self.freecompany
        }


class CharacterRaids:
    def __init__(
        self,
        endwalker: list,
        shadowbringers: list,
        stormblood: list,
        heavensward: list,
        ultimates: list,
    ) -> None:
        self.endwalker = endwalker
        self.shadowbringers = shadowbringers
        self.stormblood = stormblood
        self.heavensward = heavensward

        self.ultimates = ultimates

    # Manually formed, less pain
    def to_dict(self):
        return {
            # "endwalker": self.endwalker
            "endwalker": self.format_raids(self.endwalker),
            "shadowbringers": self.format_raids(self.shadowbringers),
            "stormblood": self.format_raids(self.stormblood),
            "heavensward": self.format_raids(self.heavensward),
            "ultimates": self.format_raids(self.ultimates),
        }

    def format_raids(self, tier: list) -> list:
        formatted_tier = {}
        for name, raid in tier.items():
            job_stats = {}
            for job in raid["allStars"]:
                format_job = {
                    "rank": job["rank"],
                    "name": job["spec"],
                    "points": int(job["points"])
                }
                if job_stats.get(job["spec"]) is None:
                    job_stats[job["spec"]]=format_job
                elif job["rank"] < job_stats.get(job["spec"])["rank"]:
                    job_stats[job["spec"]]=format_job
            formatted_tier[name]={
                "best-performance-avg": int(raid["bestPerformanceAverage"]) if raid["bestPerformanceAverage"] is not None else "-",
                "job-performance": job_stats,
                "ranking-floor-job": [
                    {
                        "best-rdps": "{:.1f}".format(floor["bestAmount"]) if floor["bestAmount"] != 0 else "-",
                        "ranking": int(floor["rankPercent"]) if floor["rankPercent"] is not None else "-",
                        "floor": floor["encounter"]["name"],
                        "job": floor["bestSpec"] if floor.get("bestSpec") is not None else "-",
                        "total-kills": floor["totalKills"]
                    }
                    for floor in raid["rankings"]
                ],
            }
        return formatted_tier