from aiohttp import ClientResponse
from typing import TYPE_CHECKING, NamedTuple, List

if TYPE_CHECKING:
    from ..Session import Session

from ..pattern import PatternManager
from ..Item import Item

store_inventory_pattern = PatternManager.getOrCompilePattern("storeInventory")


class Listing(NamedTuple):
    item: Item  # The item
    order: int  #  Item order in your store. 0 is the first listed and so on
    quantity: int  # The number of the item in your mall store.
    price: int  # The price of the item in your mall store.
    limit: int  # The limit on the item in your mall store.
    cheapest: int  # The cheapest in mall. This includes limited items, use at own risk.


def parse(html: str, **kwargs) -> List[Listing]:
    """
    Searches backoffice.php for item name, quantity, price, limit, and ID.
    """

    return [
        Listing(
            **{
                "item": Item[int(match.group(7))],
                "order": int(match.group(2)),
                "quantity": int(match.group(5)),
                "price": int(match.group(8)),
                "limit": int(match.group(10)),
                "cheapest": int(match.group(12)),
            }
        )
        for match in store_inventory_pattern.finditer(html)
    ]


def story_inventory(session: "Session") -> ClientResponse:
    """
    This class is used to get a list of items currently in a user's store
    """

    params = {"which": 1}
    return session.request("backoffice.php", params=params, parse=parse)
