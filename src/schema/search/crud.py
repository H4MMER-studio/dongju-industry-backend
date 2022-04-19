from enum import Enum


class SearchType(str, Enum):
    DELIVERY = "deliveries"
    INQUIRY = "inquiries"


class InquirySearchField(str, Enum):
    INQUIRY_TITLE = "inquiry-title"
    IQNUIRY_PERSON_NAME = "inquiry-person-name"
    INQUIRY_COMPANY_NAME = "inquiry-company-name"


class DeliverySearchField(str, Enum):
    DELIVERY_PRODUCT = "delivery-product"
    DELIVERY_SUPPLIER = "delivery-supplier"
