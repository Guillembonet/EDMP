from __future__ import absolute_import

from six.moves import xrange
import string
from random import choice

from twisted.internet import reactor
from twisted.internet.defer import succeed
from twisted.internet.task import deferLater

from Tribler.Core.Modules.wallet.wallet import Wallet, InsufficientFunds


class EnergyWallet(Wallet):
    """
    This is a dummy wallet that is primarily used for testing purposes
    """
    MONITOR_DELAY = 1

    def __init__(self):
        super(EnergyWallet, self).__init__()

        self.balance = 0
        self.created = True
        self.unlocked = True
        self.address = ''.join([choice(string.ascii_lowercase) for _ in xrange(10)])
        self.transaction_history = []

    def get_name(self):
        return 'Energy Wallet'

    def get_identifier(self):
        return 'EW'

    def create_wallet(self, *args, **kwargs):
        return succeed(None)

    def get_balance(self):
        return succeed({
            'available': self.balance,
            'pending': 0,
            'currency': self.get_identifier(),
            'precision': self.precision()
        })

    def transfer(self, quantity, hash, candidate):
        def on_balance(balance):

            self.transaction_history.append({
                'id': str(quantity),
                'outgoing': True,
                'from': self.address,
                'to': '',
                'amount': quantity,
                'fee_amount': 0.0,
                'hash': hash,
                'timestamp': '',
                'description': ''
            })

            return succeed(str(quantity))

        return self.get_balance().addCallback(on_balance)

    def monitor_transaction(self, transaction_id, hash):
        """
        Monitor an incoming transaction with a specific ID.
        """
        def on_transaction_done():
            self.transaction_history.append({
                'id': transaction_id,
                'outgoing': True,
                'from': '',
                'to': self.address,
                'amount': float(str(transaction_id)),
                'fee_amount': 0.0,
                'hash': hash,
                'timestamp': '',
                'description': ''
            })

            self.balance += float(str(transaction_id))  # txid = amount of money transferred

        if self.MONITOR_DELAY == 0:
            return succeed(None).addCallback(lambda _: on_transaction_done())
        else:
            return deferLater(reactor, self.MONITOR_DELAY, on_transaction_done)

    def get_address(self):
        return self.address

    def get_transactions(self):
        return succeed(self.transaction_history)

    def min_unit(self):
        return 1

    def precision(self):
        return 0

