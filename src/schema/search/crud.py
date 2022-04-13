from enum import Enum


class SearchType(str, Enum):
    DELIVERY = "deliveries"
    INQUIRY = "inquiries"
