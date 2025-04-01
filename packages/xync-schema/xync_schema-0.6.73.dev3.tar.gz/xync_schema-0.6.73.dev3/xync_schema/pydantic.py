from datetime import datetime
from pydantic import BaseModel

from xync_schema.enums import AdStatus, PmType, OrderStatus
from xync_schema.models import Direction, Pmcur, Cred, Actor, Pm, Ad


class _CurCoin(BaseModel):
    exid: int | str
    ticker: str
    rate: float | None = None


class CoinEpyd(_CurCoin):
    p2p: bool = True
    minimum: float | None = None


class CurEpyd(_CurCoin):
    rounding_scale: int | None = None
    minimum: int | None = None


class PmexBankPyd(BaseModel):
    id: int | None = None
    exid: str
    name: str


class PmPyd(BaseModel):
    id: int | None = None
    name: str
    identifier: str | None = None
    type_: PmType | None = None
    logo: str | None = None
    banks: list[PmexBankPyd] | None = None


# class PmcurPyd(BaseModel):
#     id: int | None = None
#     pm_id: int
#     cur_id: int


class FFiat(BaseModel):
    detail: str
    name: str | None = None
    amount: float = 0
    target: int | None = None
    banks: list[str] = []


class FiatNew(FFiat):
    cur_id: int
    pm_id: int


class FiatUpd(FFiat):
    id: int
    exid: int


class CredPydIn(BaseModel):
    id: int | None = None
    exid: int
    pmcur: Pmcur
    actor: Actor
    detail: str = ""
    name: str = ""
    banks: list[str] | None = None

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "actor", "pmcur"
        df: tuple[str, ...] = "detail", "name"
        d = self.model_dump()
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class FiatPydIn(BaseModel):
    # unq
    id: int = None
    cred: Cred
    # df
    amount: float
    target: float | None = None

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "cred"
        df: tuple[str, ...] = "amount", "target"
        d = self.model_dump()
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class BaseAd(BaseModel):
    id: int | None = None
    price: float


class BaseAdPydIn(BaseAd):
    exid: int
    min_fiat: float
    max_fiat: float | None = None
    detail: str | None = None
    auto_msg: str | None = None
    status: AdStatus = AdStatus.active
    maker: Actor = None
    direction: Direction

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "maker", "direction"
        df: tuple[str, ...] = "price", "price", "min_fiat", "max_fiat", "detail", "auto_msg", "status"
        d = self.model_dump(exclude_none=True)
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class AdBuyPydIn(BaseAdPydIn):
    pms_: list[Pm]


class AdSalePydIn(BaseAdPydIn):
    creds_: list[Cred]


class BaseOrder(BaseModel):
    id: int | None = None


class OrderPyd(BaseModel):
    id: int
    amount: float
    status: str
    actions: dict | None = {}
    cred: Cred.pyd()
    is_sell: bool
    actor: int | None = None
    created_at: datetime
    payed_at: datetime | None = None
    appealed_at: datetime | None = None
    confirmed_at: datetime | None = None
    msgs: int = 0
    topic: int


class OrderPydIn(BaseModel):
    id: int = None
    exid: int
    amount: float
    maker_topic: int | None = None
    taker_topic: int | None = None
    status: OrderStatus = OrderStatus.created
    created_at: datetime
    payed_at: datetime | None = None
    confirmed_at: datetime | None = None
    appealed_at: datetime | None = None
    ad: Ad
    cred: Cred
    taker: Actor

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> tuple[dict, dict]:
        unq: tuple[str, ...] = "id", "exid", "amount", "maker_topic", "taker_topic", "ad", "cred", "taker"
        df: tuple[str, ...] = "status", "created_at", "payed_at", "confirmed_at", "appealed_at"
        d = self.model_dump(exclude_none=True)
        return {k: getattr(self, k) for k in df if d.get(k)}, {k: getattr(self, k) for k in unq if d.get(k)}


class UreadMsgs(BaseModel):
    order_id: int
    unread_cnt: int
