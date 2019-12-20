# CORRECT DATA
POLICY_DATA = {
    'daily_limit' : 150000,
    'weeklyly_limit' : 350000,
    'monthly_limit' : 550000,
    'commission' : 0.03
}

# MISSING DATA
POLICY_DATA_NO_DAILY = {
    'weeklyly_limit' : 350000,
    'monthly_limit' : 550000,
    'commission' : 0.03
}

POLICY_DATA_NO_WEEKLY = {
    'daily_limit' : 150000,
    'monthly_limit' : 550000,
    'commission' : 0.03
}

POLICY_DATA__NO_MONTHLY = {
    'daily_limit' : 150000,
    'weeklyly_limit' : 350000,
    'commission' : 0.03
}

POLICY_DATA_NO_COMMISSION = {
    'daily_limit' : 150000,
    'weeklyly_limit' : 350000,
    'monthly_limit' : 550000,
}

# WRONG DATA TYPE
POLICY_DATA_STR_DAILY = {
    'daily_limit'  : '150000F',
    'weeklyly_limit' : 350000,
    'monthly_limit' : 550000,
    'commission' : 0.03
}

POLICY_DATA_STR_WEEKLY = {
    'daily_limit' : 150000,
    'weeklyly_limit' : '350000F',
    'monthly_limit' : 550000,
    'commission' : 0.03
}

POLICY_DATA_STR_MONTHLY = {
    'daily_limit' : 150000,
    'weeklyly_limit' : 350000,
    'monthly_limit' : '550000F',
    'commission' : 0.03
}

POLICY_DATA_STR_COMMISSION = {
    'daily_limit' : 150000,
    'weeklyly_limit' : 350000,
    'monthly_limit' : 550000,
    'commission'  : '34F'
}