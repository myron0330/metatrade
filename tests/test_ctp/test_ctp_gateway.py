# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
import json
from lib.event.event_base import EventType
from lib.event.event_engine import EventEngine
from lib.gateway.ctp_gateway import CTPMarketGateway
from lib.gateway.strategy_gateway import StrategyGateway


data = json.load(open('CTP_connect.json', 'r+'))
address = data['mdAddress']
user_id = data['userID']
password = data['password']
broker_id = data['brokerID']
address = str(address)
event_engine = EventEngine()
market_gateway = CTPMarketGateway(user_id=user_id,
                                  password=password,
                                  broker_id=broker_id,
                                  address=address,
                                  event_engine=event_engine)
strategy_gateway = StrategyGateway()
event_engine.register_handlers(EventType.event_on_tick, getattr(strategy_gateway, EventType.event_on_tick))
event_engine.start()
market_gateway.connect()
market_gateway.subscribe('rb1810')