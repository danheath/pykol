import re
from typing import Any, Dict, Tuple
from bs4 import BeautifulSoup, Tag

import libkol

from ..Error import UnknownError
from .request import Request
from ..CharacterClass import CharacterClass

pwd_pattern = re.compile(r"var pwdhash = \"([0-9a-f]+)\";")
user_id_pattern = re.compile(r"var playerid = ([0-9]+);")
username_pattern = re.compile(r"<a [^<>]*href=\"charsheet\.php\">(?:<b>)?([^<>]+)<")
characterLevel = re.compile(r"<br>Level ([0-9]+)<br>(.*?)<table")
characterHP = re.compile(
    r"onclick=\'doc\(\"hp\"\);\'[^<>]*><br><span class=[^>]+>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>"
)
characterMP = re.compile(
    r"onclick=\'doc\(\"mp\"\);\'[^<>]*><br><span class=[^>]+>([0-9]+)&nbsp;/&nbsp;([0-9]+)</span>"
)
characterMeat = re.compile(
    r"onclick=\'doc\(\"meat\"\);\'[^<>]*><br><span class=black>([0-9,]+)</span>"
)
characterAdventures = re.compile(
    r"onclick=\'doc\(\"adventures\"\);\'[^<>]*><br><span class=black>([0-9]+)</span>"
)
currentFamiliar = re.compile(
    r"href=\"familiar.php\"(?:[^>]+)>(?:<b>)?<font size=[0-9]+>(.*?)</a>(?:</b>)?, the  <b>([0-9]+)<\/b> pound (.*?)<table"
)
characterEffect = re.compile(
    r"eff\(\"[a-fA-F0-9]+\"\);\'.*?></td><td valign=center><font size=[0-9]+>(.*?) ?\(([0-9]+)\)</font><br></td>"
)
characterRonin = re.compile(r">Ronin</a>: <b>([0-9]+)</b>")
characterMindControl = re.compile(r">Mind Control</a>: <b>([0-9]{1,2})</b>")
characterDrunk = re.compile(
    r">(?:Inebriety|Temulency|Tipsiness|Drunkenness):</td><td><b>([0-9]{1,2})</b>"
)


class charpane(Request[Dict[str, Any]]):
    """
    Requests the user's character pane.
    """

    def __init__(self, session: "libkol.Session") -> None:
        super().__init__(session)

        self.request = session.request("charpane.php")

    @staticmethod
    def get_stat(soup: Tag, key: str) -> Tuple[int]:
        values = soup.find("td", text=key).next_sibling.b.stripped_strings
        return int(next(values, None)), int(next(values, "()")[1:-1])

    @classmethod
    async def parser(cls, content: str, **kwargs) -> Dict[str, Any]:
        session = kwargs["session"]  # type: "libkol.Session"

        soup = BeautifulSoup(content, "html.parser")

        pwd_matcher = pwd_pattern.search(content)
        username_matcher = username_pattern.search(content)
        user_id_matcher = user_id_pattern.search(content)

        if pwd_matcher is None or username_matcher is None or user_id_matcher is None:
            raise UnknownError("Failed to parse basic information from charpane")

        data = {
            "pwd": pwd_matcher.group(1),
            "username": username_matcher.group(1),
            "user_id": int(user_id_matcher.group(1)),
        }

        avatar = soup.find("img", crossorigin="Anonymous")
        if avatar and avatar["src"].endswith("_f.gif"):
            data["gender"] = "f"


        match = characterLevel.search(content)
        if match:
            title = str(match.group(2))
            data["level"] = int(match.group(1))
            data["level_title"] = title
            data["character_class"] = CharacterClass.from_title(title)

        match = characterHP.search(content)
        if match:
            data["current_hP"] = int(match.group(1))
            data["max_hp"] = int(match.group(2))

        match = characterMP.search(content)
        if match:
            data["current_mp"] = int(match.group(1))
            data["max_mp"] = int(match.group(2))

        match = characterMeat.search(content)
        if match:
            data["meat"] = int(match.group(1).replace(",", ""))

        data["adventures"] = int(soup.find("img", alt="Adventures Remaining").find_next_sibling("span").string)

        match = characterDrunk.search(content)
        data["inebriety"] = int(match.group(1)) if match else 0

        match = currentFamiliar.search(content)
        if match:
            data["familiar"] = {
                "name": str(match.group(1)),
                "type": str(match.group(3)),
                "weight": int(match.group(2)),
            }

        data["effects"] = [
            {"name": str(match.group(1)), "turns": int(match.group(2))}
            for match in (
                match
                for match in characterEffect.finditer(content)
                if match is not None
            )
        ]

        data["base_muscle"], data["buffed_muscle"] = cls.get_stat(soup, "Muscle:")
        data["base_moxie"], data["buffed_moxie"] = cls.get_stat(soup, "Moxie:")
        data["base_mysticality"], data["buffed_mysticality"] = cls.get_stat(soup, "Mysticality:")

        match = characterRonin.search(content)
        if match:
            data["ronin_left"] = int(match.group(1))

        match = characterMindControl.search(content)
        if match:
            data["mind_control"] = int(match.group(1))

        session.state.update(data)

        return data
