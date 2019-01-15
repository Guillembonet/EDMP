from Tribler.Core.Session import Session
from twisted.internet import reactor
from Tribler.Core.Config.tribler_config import TriblerConfig
from Tribler.community.market.core.assetamount import AssetAmount
from Tribler.community.market.core.assetpair import AssetPair
import sys


def start_market():

    if len(sys.argv) != 4:
        print('Incorrect number of arguments, using port 8080 and default state directory.')
        port = 8080
        state_dir = None
        keypair_filename = None

    else:
        port = sys.argv[1]
        state_dir = sys.argv[2]
        keypair_filename = sys.argv[3]


    config = TriblerConfig()
    config.set_http_api_port(int(port))
    config.set_http_api_enabled(True)
    config.set_bitcoinlib_enabled(True)

    if state_dir is not None:
        config.set_state_dir(state_dir)
    if keypair_filename is not None:
        config.set_trustchain_keypair_filename(keypair_filename)

    session = Session(config)
    session.start()

    if not session.lm.wallets['BTC'].created:
        print('Create bitcoin wallet')
        session.lm.wallets['BTC'].create_wallet()
    else:
        print('Bitcoin wallet already exists')

    print('Market started')
    assets = AssetPair(AssetAmount(100000, 'BTC'), AssetAmount(10, 'MB'))

    # print('Create a ask')
    # session.lm.market_community.create_ask(assets, 100)
    # print('Ask created')

    # print('Create a bid')
    # session.lm.market_community.create_bid(assets, 100)
    # print('Bid created')


reactor.callWhenRunning(start_market)
reactor.run()