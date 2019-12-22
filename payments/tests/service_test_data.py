
SERVICE_PRICE = 25000
SERVICE_PRICE_STR = '234KD0'
SERVICE_COMMISSION = 0.29
SERVICE_COMMISSION_BAD = 01.29
SERVICE_COMMISSION_BAD_2 = 0.293
SERVICE_COMMISSION_BAD_3 = 1.01

SERVICE_NAME = "TEST SERVICE"
SERVICE_NAME_EMPTY = ''
SERVICE_CUSTOMER_REFERENCE = '14587AF2514'
SERVICE_REFERENCE_NUMBER   = 14781254
SERVICE_ISSUED_AT          = "2019-07-23"
SERVICE_ISSUED_AT_BAD_DD_MM_YYYY  = "23-07-2019"
SERVICE_ISSUED_AT_BAD_MM_DD_YYYY  = "07-23-2019"
SERVICE_ISSUED_AT_BAD             = "20190723"
SERVICE_DESCRIPTION        = 'TEST SERVICE DESCRIPTION'
PAYMENT_NEW_SERVICE_URL    = 'payments:new-service'


SERVICE_DATA_INITIAL = {
        'name' : SERVICE_NAME,
        'operator' : None,
        'customer' : None,
        'category' : None,
        'service_instance': None,
        'customer_reference' : SERVICE_CUSTOMER_REFERENCE,
        'reference_number'  : SERVICE_REFERENCE_NUMBER,
        'price' : SERVICE_PRICE,
        'description' : SERVICE_DESCRIPTION,
        'issued_at'  : SERVICE_ISSUED_AT,
        'commission' : SERVICE_COMMISSION
}


