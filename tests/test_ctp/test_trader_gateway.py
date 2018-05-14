# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File:
# **********************************************************************************#
import json

from lib.event.event_base import EventType
from lib.event.event_engine import EventEngine
from lib.gateway.ctpGateway.trader_gateway import CtpTraderGateway
from lib.gateway.strategy_gateway import StrategyGateway

data = json.load(open('CTP_connect.json', 'r+'))
address = str(data['tdAddress'])
user_id = str(data['userID'])
password = str(data['password'])
broker_id = str(data['brokerID'])
address = str(address)
event_engine = EventEngine()
trader_gateway = CtpTraderGateway(user_id=user_id,
                                  password=password,
                                  broker_id=broker_id,
                                  address=address,
                                  event_engine=event_engine)
strategy_gateway = StrategyGateway()
event_engine.register_handlers(EventType.event_on_tick, getattr(strategy_gateway, EventType.event_on_tick))
event_engine.start()
trader_gateway.connect()
trader_gateway.query_account_info()