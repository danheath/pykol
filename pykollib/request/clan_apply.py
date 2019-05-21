from aiohttp import ClientResponse
from typing import OrderedTuple, TYPE_CHECKING

from ..Error import CannotChangeClanError

if TYPE_CHECKING:
    from ..Session import Session


class Response(OrderedTuple):
    success: bool
    already_member: bool


def parse(html: str, session: "Session", **kwargs) -> Response:
    """
    Formats the clan application response
    """

    if (
        "You can't apply to a new clan when you're the leader of an existing clan."
        in html
    ):
        raise CannotChangeClanError(
            "Cannot apply to another clan because you are the leader of {}".format(
                session.state.get("clan_name", "unknown")
            )
        )

    accepted = "clanhalltop.gif" in html
    already_member = "You can't apply to a clan you're already in." in html

    return {"success": accepted or already_member, "already_member": already_member}


def clan_apply(session: "Session", clan_id: int) -> ClientResponse:
    """
    Apply to a clan

    :param clan_id: id of clan
    """

    payload = {
        "recruiter": 1,
        "pwd": session.pwd,
        "whichclan": clan_id,
        "action": "joinclan",
        "apply": "Apply+to+this+Clan",
        "confirm": "on",
    }

    return session.request("showclan.php", data=payload, parse=parse)
