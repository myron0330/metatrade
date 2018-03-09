# -*- coding: utf-8 -*-
import json
import numpy as np
from .. const import (
    DEFAULT_FILLED_AMOUNT,
    DEFAULT_FILLED_TIME,
    DEFAULT_TRANSACT_PRICE,
)
from uuid import uuid1


def _get_date_hash(date):
    return date[:10]


class OrderStateMessage(object):
    """
    Enums: Order state message.
    """
    TO_FILL = u'待挂单'
    OPEN = u'待成交'
    UP_LIMIT = u'证券涨停'
    DOWN_LIMIT = u'证券跌停'
    PARTIAL_FILLED = u'部分成交'
    FILLED = u'全部成交'
    SELLOUT = u'无可卖头寸或现金'
    NO_AMOUNT = u'当日无成交量'
    NO_NAV = u'当日无净值'
    PRICE_UNCOVER = u'限价单价格未到'
    CANCELED = u'已撤单'
    NINC_HALT = u'证券代码不满足条件或证券停牌'
    TYPE_ERROR = u'订单类型错误'
    TO_CANCEL = u'待撤单'
    FAILED = u'系统错误'
    INVALID_PRICE = u'限价单价格越界'
    INACTIVE = u'证券已下市'
    INVALID_SYMBOL = u'下单合约非法'
    NO_ENOUGH_CASH = u'可用现金不足'
    NO_ENOUGH_MARGIN = u'可用保证金不足'
    NO_ENOUGH_AMOUNT = u'可用持仓不足'
    NO_ENOUGH_CLOSE_AMOUNT = u'可平持仓数量不足'
    NO_ENOUGH_SHARE = u'可赎回份额不足'
    INVALID_AMOUNT = u'下单数量非法'
    INVALID_PORTFOLIO = u'订单无对应组合持仓'


class OrderState(object):
    """
    Enums: Order state.
    """
    ORDER_SUBMITTED = 'ORDER_SUBMITTED'
    CANCEL_SUBMITTED = 'CANCEL_SUBMITTED'
    OPEN = 'OPEN'
    PARTIAL_FILLED = 'PARTIAL_FILLED'
    FILLED = 'FILLED'
    REJECTED = 'REJECTED'
    CANCELED = 'CANCELED'
    ERROR = 'ERROR'

    INACTIVE = [FILLED, REJECTED, CANCELED, ERROR]
    ACTIVE = [ORDER_SUBMITTED, CANCEL_SUBMITTED, OPEN, PARTIAL_FILLED]
    ALL = [ORDER_SUBMITTED, CANCEL_SUBMITTED, OPEN, PARTIAL_FILLED, FILLED, REJECTED, CANCELED, ERROR]


class BaseOrder(object):

    def __init__(self, symbol, order_amount, order_time=None, direction=None, order_type='market', price=0.,
                 order_id=None, state=OrderState.ORDER_SUBMITTED):
        self._symbol = symbol
        self._order_amount = abs(order_amount)
        self._order_time = order_time
        self._direction = direction
        self._order_type = order_type
        self._price = price
        self._state = state
        self._state_message = OrderStateMessage.TO_FILL
        self._order_id = order_id
        self._filled_time = DEFAULT_FILLED_TIME
        self._filled_amount = DEFAULT_FILLED_AMOUNT
        self._transact_price = DEFAULT_TRANSACT_PRICE
        self._slippage = 0.
        self._commission = 0.

    @property
    def symbol(self):
        return self._symbol

    @property
    def order_amount(self):
        return self._order_amount

    @property
    def order_time(self):
        return self._order_time

    @property
    def direction(self):
        return self._direction

    @property
    def price(self):
        return self._price

    @property
    def state(self):
        return self._state

    @property
    def state_message(self):
        return self._state_message

    @property
    def order_id(self):
        return self._order_id

    @property
    def filled_time(self):
        return self._filled_time

    @property
    def filled_amount(self):
        return self._filled_amount

    @property
    def transact_price(self):
        return self._transact_price

    @property
    def open_amount(self):
        return self._order_amount - self._filled_amount

    @property
    def commission(self):
        return self._commission

    @property
    def slippage(self):
        return self._slippage

    @symbol.setter
    def symbol(self, *args):
        raise AttributeError('Exception in "BaseOrder.symbol": user must not modify order.symbol!')

    @order_amount.setter
    def order_amount(self, *args):
        raise AttributeError('Exception in "BaseOrder.order_amount": user must not modify order.order_amount!')

    @order_time.setter
    def order_time(self, *args):
        raise AttributeError('Exception in "BaseOrder.order_time": user must not modify order.order_time!')

    @direction.setter
    def direction(self, *args):
        raise AttributeError('Exception in "BaseOrder.direction": user must not modify order.direction!')

    @price.setter
    def price(self, *args):
        raise AttributeError('Exception in "BaseOrder.price": User must not modify order.price!')

    @state.setter
    def state(self, *args):
        raise AttributeError('Exception in "BaseOrder.state": user must not modify order.state!')

    @state_message.setter
    def state_message(self, *args):
        raise AttributeError('Exception in "BaseOrder.state_message": user must not modify order.state_message!')

    @order_id.setter
    def order_id(self, *args):
        raise AttributeError('Exception in "BaseOrder.order_id": User must not modify order.order_id!')

    @filled_time.setter
    def filled_time(self, *args):
        raise AttributeError('Exception in "BaseOrder.filled_time": user must not modify order.filled_time!')

    @filled_amount.setter
    def filled_amount(self, *args):
        raise AttributeError('Exception in "BaseOrder.filled_amount": user must not modify order.filled_amount!')

    @transact_price.setter
    def transact_price(self, *args):
        raise AttributeError('Exception in "BaseOrder.transact_price": User must not modify order.transact_price!')

    @commission.setter
    def commission(self, *args):
        raise AttributeError('Exception in "Order.commission": User must not modify order.commission!')

    @slippage.setter
    def slippage(self, *args):
        raise AttributeError('Exception in "Order.slippage": User must not modify Order.slippage!')

    def __repr__(self):
        repr_dict = {key: unicode(value) for key, value in self.__dict__.iteritems()}
        return ''.join(['Order', json.dumps(repr_dict).replace('"_', '').replace('"', '').replace('{', '(').
                       replace('}', ')').replace('null', 'None')])


class Order(BaseOrder):
    """
    Order instance.
    """
    __cur_date__, __max_order_id__ = None, 1

    __slots__ = [
        '_portfolio_id',
        '_order_id',
        '_symbol',
        '_order_amount',
        '_filled_amount',
        '_order_time',
        '_filled_time',
        '_order_type',
        '_price',
        '_transact_price',
        '_turnover_value',
        '_direction',
        '_offset_flag',
        '_commission',
        '_slippage',
        '_state',
        '_state_message',
    ]

    def __getstate__(self):
        return dict(
            (slot, getattr(self, slot))
            for slot in self.__slots__
            if hasattr(self, slot)
        )

    def __setstate__(self, state):
        for slot, value in state.items():
            setattr(self, slot, value)

    def __init__(self, symbol, amount, order_time=None, order_type='market', price=0.,
                 portfolio_id=None, order_id=None, offset_flag=None, direction=None,
                 **kwargs):
        super(Order, self).__init__(symbol=symbol, order_amount=amount, order_time=order_time,
                                    order_type=order_type, price=price)
        self._order_id = order_id if order_id is not None else str(uuid1())
        self._portfolio_id = portfolio_id
        self._direction = direction if direction is not None else amount/abs(amount) if amount != 0 else 0
        self._turnover_value = 0.
        self._offset_flag = offset_flag or 'open' if np.sign(amount) == 1 else 'close'

    @property
    def offset_flag(self):
        return self._offset_flag

    @property
    def order_type(self):
        return self._order_type

    @property
    def turnover_value(self):
        return self._turnover_value

    @property
    def portfolio_id(self):
        return self._portfolio_id

    def to_dict(self):
        """
        To dict
        """
        return self.__dict__

    @classmethod
    def from_request(cls, request):
        """
        Generate new order from request

        Args:
            request(dict): request database
        """
        return cls(**request)

    @classmethod
    def from_query(cls, query_data):
        """
        Recover existed order from query database

        Args:
            query_data(dict): query database
        """
        query_data['amount'] = query_data.pop('order_amount')
        order = cls(**query_data)
        order._filled_time = query_data['filled_time']
        order._state = query_data['state']
        order._state_message = query_data['state_message']
        order._commission = query_data['commission']
        order._slippage = query_data['slippage']
        order._turnover_value = query_data['turnover_value']
        order._filled_amount = query_data['filled_amount']
        order._transact_price = query_data['transact_price']
        order._direction = query_data.get('direction', 1)
        return order

    @property
    def __dict__(self):
        mapper = (lambda x: x.strip('_'))
        return {mapper(key): getattr(self, key) for key in self.__slots__}

    def __repr__(self):
        return ''.join(['Order', json.dumps(self.__dict__).replace('"_', '').replace('"', '').replace('{', '(').
                       replace('}', ')').replace('null', 'None')])


class DigitalCurrencyOrder(ValueObject):

    __slots__ = ['symbol',
                 'amount',
                 'order_time',
                 'order_type',
                 'price',
                 'state',
                 'state_message',
                 'order_id',
                 'account_id',
                 'filled_time',
                 'filled_amount',
                 'transact_price',
                 'fee',
                 'fee_currency',
                 'side',
                 'direction',
                 'turnover_value',
                 'exchange']

    def __init__(self, symbol, amount, order_time=None, order_type='market', price=0.,
                 state=OrderState.ORDER_SUBMITTED, state_message=OrderStateMessage.TO_FILL,
                 order_id=None, account_id=None, filled_time=None, filled_amount=None,
                 transact_price=None, fee=None, fee_currency=None,
                 side=None, direction=None, turnover_value=None, exchange=None):
        self.symbol = symbol
        self.amount = amount
        self.order_time = order_time
        self.order_type = order_type
        self.price = price
        self.state = state
        self.state_message = state_message
        self.order_id = order_id or str(uuid1())
        self.account_id = account_id
        self.filled_time = filled_time
        self.filled_amount = filled_amount
        self.transact_price = transact_price
        self.fee = fee
        self.fee_currency = fee_currency
        self.side = side or ('BUY' if np.sign(amount) == 1 else 'SELL')
        self.direction = direction or (amount/abs(amount) if amount != 0 else 0)
        self.turnover_value = turnover_value
        self.exchange = exchange

    def update_from_subscribe(self, item):
        """
        Update from subscribe.
        """
        order_state_map = {
            'PENDING_NEW': OrderState.ORDER_SUBMITTED,
            'NEW': OrderState.OPEN,
            'PARTIALLY_FILLED': OrderState.PARTIAL_FILLED,
            'FILLED': OrderState.FILLED,
            'REJECTED': OrderState.REJECTED,
            'CANCELED': OrderState.CANCELED
        }
        order_state_message_map = {
            'PENDING_NEW': OrderStateMessage.TO_FILL,
            'NEW': OrderStateMessage.OPEN,
            'PARTIALLY_FILLED': OrderStateMessage.PARTIAL_FILLED,
            'FILLED': OrderStateMessage.FILLED,
            'REJECTED': OrderStateMessage.REJECT,
            'CANCELED': OrderStateMessage.CANCELED
        }
        self.state = order_state_map[item['orderStatus']]
        self.state_message = order_state_message_map[item['orderStatus']]
        self.exchange = item['exchange']
        self.price = item['price']
        self.filled_amount = item['filled']
        self.transact_price = item['avgPrice']
        self.fee = item['fee']
        self.fee_currency = item['feeCurrency']
        self.turnover_value = item['cost']

    def to_request(self):
        """
        To exchange request.
        """
        return {
            'orderType': self.order_type.upper(),
            'symbol': self.symbol.split('.')[0],
            'side': self.side,
            'price': self.price,
            'amount': self.amount,
            'extOrdId': self.order_id
        }

    def __repr__(self):
        content = ', '.join(['{}: {{}}'.format(item) for item in self.__slots__]).format(
            self.symbol, self.amount, self.order_time, self.order_type, self.price, self.state,
            self.state_message.encode('utf-8'), self.order_id, self.account_id, self.filled_time,
            self.filled_amount, self.transact_price, self.fee, self.fee_currency, self.side,
            self.direction, self.turnover_value, self.exchange
        )
        return 'DigitalCurrencyOrder({})'.format(content)
