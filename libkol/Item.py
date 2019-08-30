import asyncio
from tortoise.fields import (
    IntField,
    CharField,
    BooleanField,
    ForeignKeyField,
    ManyToManyField,
)
from tortoise.models import ModelMeta
from tortoise.exceptions import DoesNotExist
from typing import Coroutine, List, Optional, Union, Tuple
import re
import time
from statistics import mean

import libkol
from libkol import request
from .CharacterClass import CharacterClass
from .Slot import Slot
from .Stat import Stat
from .Model import Model
from .Error import ItemNotFoundError, WrongKindOfItemError
from .util import EnumField, parsing
from . import types


class ItemMeta(ModelMeta):
    def __getitem__(self, key: Union[int, str]):
        """
        Syntactic sugar for synchronously grabbing an item by id, description id or name.

        :param key: id, desc_id or name of item you want to grab
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        async def getitem():
            result = None
            try:
                if isinstance(key, int):
                    # Most desc_ids are 9 digits but there are 14 that aren't.
                    # At time of writing this is good for 115,100 new items before any collisions.
                    if key == 31337 or key == 46522 or key >= 125353:
                        result = await self.get_or_discover(desc_id=key)
                    else:
                        result = await self.get_or_discover(id=key)
                else:
                    result = await self.get(name=key)
                future.set_result(result)
                
            except DoesNotExist:
                future.set_exception(ItemNotFoundError(f"Cannot find an item with the token `{key}`"))

        asyncio.ensure_future(getitem())
        return future


class Item(Model, metaclass=ItemMeta):
    id: int = IntField(pk=True, generated=False)  # type: ignore
    name: str = CharField(max_length=255)  # type: ignore
    desc_id: int = IntField()  # type: ignore
    plural: str = CharField(max_length=255, null=True)  # type: ignore
    image: str = CharField(max_length=255)  # type: ignore
    autosell_value: int = IntField(default=0)  # type: ignore
    level_required: int = IntField(default=0)  # type: ignore

    # Consumables
    food: bool = BooleanField(default=False)  # type: ignore
    fullness: int = IntField(default=0)  # type: ignore
    booze: bool = BooleanField(default=False)  # type: ignore
    inebriety: int = IntField(default=0)  # type: ignore
    spleen: bool = BooleanField(default=False)  # type: ignore
    spleenhit: int = IntField(default=0)  # type: ignore
    quality: str = CharField(max_length=255, null=True)  # type: ignore
    gained_adventures_min: int = IntField(default=0)  # type: ignore
    gained_adventures_max: int = IntField(default=0)  # type: ignore
    gained_muscle_min: int = IntField(default=0)  # type: ignore
    gained_muscle_max: int = IntField(default=0)  # type: ignore
    gained_mysticality_min: int = IntField(default=0)  # type: ignore
    gained_mysticality_max: int = IntField(default=0)  # type: ignore
    gained_moxie_min: int = IntField(default=0)  # type: ignore
    gained_moxie_max: int = IntField(default=0)  # type: ignore

    # Usability
    usable: bool = BooleanField(default=False)  # type: ignore
    multiusable: bool = BooleanField(default=False)  # type: ignore
    combat_usable: bool = BooleanField(default=False)  # type: ignore
    reusable: bool = BooleanField(default=False)  # type: ignore
    combat_reusable: bool = BooleanField(default=False)  # type: ignore
    # Can be used on others
    curse: bool = BooleanField(default=False)  # type: ignore

    # Equipment
    hat: bool = BooleanField(default=False)  # type: ignore
    pants: bool = BooleanField(default=False)  # type: ignore
    shirt: bool = BooleanField(default=False)  # type: ignore
    weapon: bool = BooleanField(default=False)  # type: ignore
    weapon_hands: Optional[int] = IntField(null=True)  # type: ignore
    weapon_type: Optional[str] = CharField(max_length=255, null=True)  # type: ignore
    offhand: bool = BooleanField(default=False)  # type: ignore
    offhand_type: Optional[str] = CharField(max_length=255, null=True)  # type: ignore
    accessory: bool = BooleanField(default=False)  # type: ignore
    container: bool = BooleanField(default=False)  # type: ignore
    sixgun: bool = BooleanField(default=False)  # type: ignore
    familiar_equipment: bool = BooleanField(default=False)  # type: ignore
    power: Optional[int] = IntField(null=True)  # type: ignore
    required_muscle: int = IntField(default=0)  # type: ignore
    required_mysticality: int = IntField(default=0)  # type: ignore
    required_moxie: int = IntField(default=0)  # type: ignore
    required_class: Optional[CharacterClass] = EnumField(enum_type=CharacterClass, null=True)  # type: ignore
    notes: str = CharField(max_length=255, default="")  # type: ignore

    # Collections
    foldgroup: Optional["libkol.FoldGroup"] = ForeignKeyField("models.FoldGroup", related_name="items", null=True)  # type: ignore
    foldgroup_id: Optional[int]
    zapgroup: Optional["libkol.ZapGroup"] = ForeignKeyField("models.ZapGroup", related_name="items", null=True)  # type: ignore
    zapgroup_id: Optional[int]

    outfit_variants = ManyToManyField(
        "models.OutfitVariant", related_name="pieces", null=True
    )

    # NPC Store Info
    store_row: Optional[int] = IntField(null=True)  # type: ignore
    store_price: Optional[int] = IntField(null=True)  # type: ignore
    store: Optional["libkol.Store"] = ForeignKeyField("models.Store", related_name="items", null=True)  # type: ignore
    store_id: Optional[int]

    # Flags
    hatchling: bool = BooleanField(default=False)  # type: ignore
    pokepill: bool = BooleanField(default=False)  # type: ignore
    sticker: bool = BooleanField(default=False)  # type: ignore
    card: bool = BooleanField(default=False)  # type: ignore
    folder: bool = BooleanField(default=False)  # type: ignore
    bootspur: bool = BooleanField(default=False)  # type: ignore
    bootskin: bool = BooleanField(default=False)  # type: ignore
    food_helper: bool = BooleanField(default=False)  # type: ignore
    booze_helper: bool = BooleanField(default=False)  # type: ignore
    guardian: bool = BooleanField(default=False)  # type: ignore
    single_equip: bool = BooleanField(default=True)  # type: ignore
    # Can appear as a bounty item
    bounty: bool = BooleanField(default=False)  # type: ignore
    # 0: n/a, 1: simple, 2: complex
    candy: int = IntField()  # type: ignore
    # What is this for?
    sphere: bool = BooleanField(default=False)  # type: ignore
    # is a quest item
    quest: bool = BooleanField(default=False)  # type: ignore
    # is a gift item
    gift: bool = BooleanField(default=False)  # type: ignore
    # is tradeable
    tradeable: bool = BooleanField(default=False)  # type: ignore
    # is discardable
    discardable: bool = BooleanField(default=False)  # type: ignore
    # is considered salad when consumed
    salad: bool = BooleanField(default=False)  # type: ignore
    # is considered beer when consumed
    beer: bool = BooleanField(default=False)  # type: ignore
    # is considered wine when consumed
    wine: bool = BooleanField(default=False)  # type: ignore
    # is considered martini when consumed
    martini: bool = BooleanField(default=False)  # type: ignore
    # is considered saucy when consumed
    saucy: bool = BooleanField(default=False)  # type: ignore
    # is considered lasagna when consumed
    lasagna: bool = BooleanField(default=False)  # type: ignore
    # is considered pasta when consumed
    pasta: bool = BooleanField(default=False)  # type: ignore

    @property
    def adventures(self):
        return (self.gained_adventures_min + self.gained_adventures_max) / 2

    def pluralize(self):
        return "{}s".format(self.name) if self.plural is None else self.plural

    @property
    def space(self):
        s = (
            self.fullness
            if self.food
            else self.inebriety
            if self.booze
            else self.spleenhit
            if self.spleen
            else None
        )

        if s is None:
            raise WrongKindOfItemError("You cannot consume this item")

        return s

    async def autosell(self, quantity: int = 1):
        return await request.autosell_items(self.kol, [self]).parse()

    @property
    def cleans_organ(self) -> Optional[Tuple[int, str]]:
        m = re.match(r"-(\d+) spleen", self.notes)

        if m is None:
            return None

        return (int(m.group(1)), "spleen")

    async def consume(self, utensil: Optional["Item"] = None) -> parsing.ResourceGain:
        if self.food:
            return await request.eat(self.kol, self, utensil=utensil).parse()
        elif self.booze:
            return await request.drink(self.kol, self, utensil=utensil).parse()
        elif self.spleen:
            return await request.chew(self.kol, self).parse()
        else:
            raise WrongKindOfItemError("You cannot consume this item")

    @classmethod
    async def get_or_discover(cls, *args, **kwargs) -> "Item":
        result = await cls.filter(*args, **kwargs).first()

        if result is None:
            id: int = kwargs.get("id", None)
            desc_id: int = kwargs.get("desc_id", None)

            return await cls.discover(id=id, desc_id=desc_id)

        return result

    @classmethod
    async def discover(cls, id: int = None, desc_id: int = None):
        """
        Discover this item using its id or description id. The description id is preferred as
        it provides more information, so if only an id is provided, libkol will first determine
        the desc_id.

        Note that this Returns an Item object but it is not automatically committed to the database.

        :param id: Id of the item to discover
        :param desc_id: Description id of the item to discover
        """
        if id is not None:
            desc_id = (await request.item_information(cls.kol, id).parse()).descid

        if desc_id is None:
            raise ItemNotFoundError(
                "Cannot discover an item without either an id or a desc_id"
            )

        info = await request.item_description(cls.kol, desc_id).parse()
        return Item(**{k: v for k, v in info.items() if v is not None})

    @property
    def type(self):
        types = [
            "hat",
            "shirt",
            "weapon",
            "offhand",
            "pants",
            "familiar_equipment",
            "accessory",
        ]
        return next((t for t in types if getattr(self, t)), "other")

    @property
    def slot(self) -> Optional[Slot]:
        return Slot.from_db(self.type)

    async def get_description(self):
        return await request.item_description(self.kol, self.desc_id).parse()

    async def get_mall_price(self, limited: bool = False) -> Optional[int]:
        """
        Get the lowest price for this item in the mall

        :param limited: Include limited sales in this search
        """
        prices = await request.mall_price(self.kol, self).parse()

        if limited and len(prices.limited) > 0:
            return prices.limited[0].price

        if len(prices.unlimited) > 0:
            return prices.unlimited[0].price

        return None

    async def get_cf_price(self, days: int = 30) -> Optional[int]:
        """
        Get the average transaction price from Coldfront logs

        :param days: Number of days of transactions to consider (default 30)
        """
        ts = int(time.time())
        params = {
            "itemid": self.id,
            "starttime": ts - 60 * 68 * 24 * days,
            "endtime": ts,
        }
        response = await self.kol.request(
            "http://kol.coldfront.net/newmarket/translist.php", "GET", params=params
        )
        result = await response.text()

        transactions = [
            parsing.to_float(t[(t.rfind("@") + 1) :])
            for t in result[result.find("\n") :].split("\n")
            if t not in ["", "."]
        ]

        return int(mean(transactions)) if len(transactions) > 0 else None

    async def get_mall_listings(self, **kwargs) -> List["types.Listing"]:
        return await request.mall_search(self.kol, query=self, **kwargs).parse()

    async def buy_from_mall(
        self,
        listing: "types.Listing" = None,
        store_id: int = None,
        price: int = 0,
        quantity: int = 1,
    ):
        if listing is None and store_id is None:
            listings = await self.get_mall_listings(
                num_results=quantity, max_price=price
            )

            tasks = []  # type: List[Coroutine]

            for l in listings:
                q = min(quantity, (l.limit if l.limit > 0 else quantity), l.stock)
                tasks += [
                    request.mall_purchase(
                        self.kol, item=self, listing=l, quantity=q
                    ).parse()
                ]
                quantity -= q

            return await asyncio.gather(*tasks)

        return await request.mall_purchase(
            self.kol,
            item=self,
            listing=listing,
            store_id=store_id,
            price=price,
            quantity=quantity,
        ).parse()

    async def acquire(self, quantity: int = 1):
        need = quantity - self.amount

        if need > 0:
            await self.buy_from_mall(quantity=need)

        return True

    @property
    def amount(self):
        return self.kol.inventory[self] + list(self.kol.equipment.values()).count(self)

    def equipped(self):
        return self in self.kol.equipment.values()

    async def equip(self, slot: Optional[Slot] = None) -> bool:
        actual_slot = self.slot if slot is None else slot

        if actual_slot is None:
            raise WrongKindOfItemError("This item cannot be equipped")

        curr = self.kol.equipment

        # If it's already there don't worry
        if curr[actual_slot] == self:
            return True

        # If user didn't specify an accessory and we have it in a slot, don't worry
        if (
            actual_slot is Slot.Acc1
            and slot is None
            and (curr[Slot.Acc2] == self or curr[Slot.Acc3] == self)
        ):
            return True

        return await request.equip(self.kol, self, actual_slot).parse()

    def have(self):
        return self.amount > 0

    def meet_requirements(self):
        return (
            self.kol.level >= self.level_required
            and self.kol.get_stat(Stat.Muscle) >= self.required_muscle
            and self.kol.get_stat(Stat.Mysticality) >= self.required_mysticality
            and self.kol.get_stat(Stat.Moxie) >= self.required_moxie
        )

    async def use(self, quantity: int = 1, multi_use: bool = True):
        if self.usable is False:
            raise WrongKindOfItemError("This item cannot be used")

        if self.multiusable and multi_use and quantity > 1:
            await request.item_multi_use(self.kol, self, quantity).parse()
            return

        tasks = [request.item_use(self.kol, self).parse() for _ in range(quantity)]
        return await asyncio.gather(*tasks)
