from Tribler.Core.Session import Session
from twisted.internet import reactor
from Tribler.Core.Config.tribler_config import TriblerConfig
from Tribler.community.market.core.assetamount import AssetAmount
from Tribler.community.market.core.assetpair import AssetPair


def start_market():

    config = TriblerConfig()
    config.set_http_api_port(8082)
    config.set_http_api_enabled(True)
    config.set_bitcoinlib_enabled(True)
    print(config.get_is_matchmaker())
    config.set_state_dir('/home/bunetz/.TriblerTmp')
    session = Session(config)
    session.start()

    if not session.lm.wallets['BTC'].created:
        print('Create bitcoin wallet')
        session.lm.wallets['BTC'].create_wallet()
    else:
        print('Bitcoin wallet already exists')

    print('Market started')
    assets = AssetPair(AssetAmount(100000, 'BTC'), AssetAmount(10, 'MB'))

    print('Create a ask')
    session.lm.market_community.create_ask(assets, 100)
    print('Ask created')

    # print('Create a bid')
    # session.lm.market_community.create_bid(assets, 100)
    # print('Bid created')


reactor.callWhenRunning(start_market)
reactor.run()