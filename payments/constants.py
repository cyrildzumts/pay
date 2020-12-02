

HELP_TEXT_FOR_DATE ="Please use the following format: <em>YYYY-MM-DD</em>."
HELP_TEXT_FOR_SERVICE_REF_NUMBER = 'Please enter the reference number issued by the operation.'
HELP_TEXT_FOR_OPERATOR = 'Please enter the operator who is offering this service'
help_text=HELP_TEXT_FOR_CUSTOMER = 'Please enter the customer who is using this service'
help_text=HELP_TEXT_FOR_CUSTOMER_REF = 'Please enter the customer reference number used by the operator of this service'
help_text=HELP_TEXT_FOR_SERVICE_ISSUED_AT = 'Please enter the date when this bill was issued (following format: <em>YYYY-MM-DD</em>.)'

COMMISSION_DEFAULT = 0.03
COMMISSION_MAX_DIGITS = 7
COMMISSION_DECIMAL_PLACES = 5

POLICY_GROUP_BASIC = 0
POLICY_GROUP_SILVER = 1
POLICY_GROUP_GOLD = 2

POLICY_GROUP = (
    (POLICY_GROUP_BASIC, 'BASIC'),
    (POLICY_GROUP_SILVER, 'SILVER'),
    (POLICY_GROUP_GOLD, 'GOLD')
)

PR_ACTIVE           = 'Active'
PR_CANCELED         = 'Canceled'
PR_CLEARED          = 'Cleared'
PR_ACCEPTED         = 'Accepted'
PR_CREATED          = 'Created'
PR_COMPLETED        = 'Completed'
PR_DECLINED         = 'Declined'
PR_EXPIRED          = 'Expired'
PR_FAILED           = 'Failed'
PR_PAID             = 'Paid'
PR_PROCESSED        = 'Processed'
PR_PENDING          = 'Pending'
PR_REFUSED          = 'Refused'
PR_REVERSED         = 'Reversed'

PR_STATUS = [
    PR_ACCEPTED,PR_ACTIVE, PR_CANCELED, PR_CLEARED,
    PR_COMPLETED, PR_CREATED, PR_DECLINED, PR_EXPIRED,
    PR_FAILED, PR_PAID, PR_PENDING, PR_PROCESSED, 
    PR_REFUSED, PR_REVERSED
]