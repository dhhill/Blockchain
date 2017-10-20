import hashlib, json, sys
import random
random.seed(0)

def hashMe(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg) != str:
        msg = json.dumps(msg,sort_keys=True)    # if we don't sort keys, we can't guarantee repeatability!

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


def makeTransaction(maxValue=3):
    # This will create valid transactions in the range of (1,maxValue)
    sign = int(random.getrandbits(1))*2 - 1     # this will randomly choose -1 or 1
    amount = random.randint(1,maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays
    # by construction, this will always return transactions that respect the conservation of tokens
    # however, note that we have not done anything to check whther these overdraft an account
    return {u'Alice':alicePays,u'Bob':bobPays}

txnBuffer = [makeTransaction() for i in range(30)]

def updateState(txn, state):
    # Inputs: txn, state: dictionaries keyed with account names, holding numeric values for the transfer amount (txn) or account balance (state)
    # Returns: Updated state, with additional users added to state if necessary
    # NOTE: This does not validate the transaction- just updates the state!

    # If the transaction is valid, then update the state
    state = state.copy()    # As dictionaries are mutable, let's avoid any confusion by reating a vorking copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state

def isValidTxn(txn, state):
    # assume that the transaction is a dictionary keyed by account names

    #check that the sum of the deposits and withdrawals is 0
    if sum(txn.values()) is not 0:
        return False

    # Check that the transaction does not cause an overdraft
    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False

    return True

state = {u'Alice':5,u'Bob':5}

print(isValidTxn({u'Alice':-3,u'Bob':3},state))
print(isValidTxn({u'Alice':-4,u'Bob':3},state))
print(isValidTxn({u'Alice':-6,u'Bob':6},state))
print(isValidTxn({u'Alice':-4,u'Bob':2,u'Lisa':2},state))
print(isValidTxn({u'Alice':-4,u'Bob':3,u'Lisa':2},state))
