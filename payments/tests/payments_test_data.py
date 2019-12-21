PAYMENT_AMOUNT = 15000
PAYMENT_DESCRIPTION = 'PAYMENT TEST DESCRIPTION'

PAYMENT_DATA_INITIAL = {
    'amount' : PAYMENT_AMOUNT,
    'sender' : None,
    'recipient' : None,
    'details' : PAYMENT_DESCRIPTION
}

PAYMENT_DATA_NO_DETAIL = {
    'amount' : PAYMENT_AMOUNT,
    'sender' : None,
    'recipient' : None,
    'details' : None
}

PAYMENT_DATA_MISSING_DETAIL = {
    'amount' : PAYMENT_AMOUNT,
    'sender' : None,
    'recipient' : None,
}

PAYMENT_DATA_NO_AMOUNT = {
    'amount' : None,
    'sender' : None,
    'recipient' : None,
    'details' : PAYMENT_DESCRIPTION
}

PAYMENT_DATA_MISSING_AMOUNT = {
    'sender' : None,
    'recipient' : None,
    'details' : PAYMENT_DESCRIPTION
}

PAYMENT_DATA_MISSING_SENDER = {
    'amount' : PAYMENT_AMOUNT,
    'recipient' : None,
    'details' : PAYMENT_DESCRIPTION
}

PAYMENT_DATA_MISSING_RECIPIENT = {
    'amount' : PAYMENT_AMOUNT,
    'sender' : None,
    'details' : PAYMENT_DESCRIPTION
}