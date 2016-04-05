import stripe
from time import time

def gentok(object_type=None, fail=False, mod_params={}):

    object_type = "card" if not object_type else object_type.lower()

    card_details = {
        'number': '4242424242424242',
        'cvc': '123',
        'exp_month': 12,
        'exp_year': 2019,
    }

    bank_details = {
        'country': 'US',
        'currency': 'usd',
        'account_holder_name': 'First Last',
        'account_holder_type': 'individual',
        'routing_number': '110000000',
        'account_number': '000123456789'
    }

    if object_type in ['card']:
        if fail:
            card_details.update({'number': '4000000000000341'})
        card_details.update(mod_params)
        return stripe.Token.create(card=card_details)

    if object_type[:3] in ['deb']:
        card_details.update({
            'number': '4000056655665556',
            'address_country': 'US',
            'currency': 'usd'
        })
        if fail:
            card_details.update({'number': '4000056655665564'})
        card_details.update(mod_params)
        return stripe.Token.create(card=card_details)

    if object_type[:4] in ['bank']:
        if fail:
            bank_details.update({'account_number': '000222222227'})
        bank_details.update(mod_params)
        return stripe.Token.create(bank_account=bank_details)

    raise ValueError('Unable to identify type of token!')

def gentokid(*args, **kwargs):
    tok = gentok(*args, **kwargs)
    print tok
    return tok.id

def genacc(managed=True, external_accounts=None, mod_params={}):

    if not external_accounts:
        external_accounts = []

    if not isinstance(external_accounts, list):
        external_accounts = [external_accounts]

    params = {
        'managed': managed,
        'country': 'US',
        'email': str(time()) + '@test.test',
    }
    params.update(mod_params)

    acc = stripe.Account.create(**params)

    for acc_tok in external_accounts:
        acc.external_accounts.create(external_account=acc_tok)

    return stripe.Account.retrieve(acc.id)

def genaccid(*args, **kwargs):
    acc = genacc(*args, **kwargs)
    print acc
    return acc.id
