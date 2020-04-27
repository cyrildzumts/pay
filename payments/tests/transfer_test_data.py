TRANSFER_AMOUNT = 15000
TRANSFER_DESCRIPTION = 'TRANSFER TEST DESCRIPTION'

TRANSFER_DATA_INITIAL = {
    'amount' : TRANSFER_AMOUNT,
    'sender' : None,
    'recipient' : None,
    'details' : TRANSFER_DESCRIPTION
}

TRANSFER_DATA_NO_DETAIL = {
    'amount' : TRANSFER_AMOUNT,
    'sender' : None,
    'recipient' : None,
    'details' : None
}

TRANSFER_DATA_MISSING_DETAIL = {
    'amount' : TRANSFER_AMOUNT,
    'sender' : None,
    'recipient' : None,
}

TRANSFER_DATA_NO_AMOUNT = {
    'amount' : None,
    'sender' : None,
    'recipient' : None,
    'details' : TRANSFER_DESCRIPTION
}

TRANSFER_DATA_MISSING_AMOUNT = {
    'sender' : None,
    'recipient' : None,
    'details' : TRANSFER_DESCRIPTION
}

TRANSFER_DATA_MISSING_SENDER = {
    'amount' : TRANSFER_AMOUNT,
    'recipient' : None,
    'details' : TRANSFER_DESCRIPTION
}

TRANSFER_DATA_MISSING_RECIPIENT = {
    'amount' : TRANSFER_AMOUNT,
    'sender' : None,
    'details' : TRANSFER_DESCRIPTION
}