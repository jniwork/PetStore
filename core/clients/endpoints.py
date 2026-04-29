from enum import Enum


class Endpoints(Enum):
    PET = "/pet"
    PET_BY_ID = "/pet/{pet_id}"

    STORE_ORDER = "/store/order"
    STORE_ORDER_BY_ID = "/store/order/{order_id}"

    USER = "/user"
    USER_LOGIN = "/user/login"