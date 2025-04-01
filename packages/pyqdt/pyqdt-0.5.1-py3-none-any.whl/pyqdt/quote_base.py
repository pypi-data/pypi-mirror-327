# -*- coding: utf-8 -*-
import os, sys
import math
import numpy as np
import pandas as pd

from io import BytesIO
from functools import lru_cache, wraps

from .utils import *

def assert_quote_init(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        data_path = args[0].get_data_path()
        if not data_path or not os.path.exists(data_path):
            print("Quote is not initialized.")
        else:
            return func(*args, **kwargs)

    return _wrapper

class QuoteBase(object):
    def __init__(self, data_path=None):
        """本地行情数据类

        参数:
            data_path: 数据目录

        """
        if not hasattr(self, '_data_path'):
            self._data_path = ''
        if data_path:
            self.init(data_path)
        if not hasattr(self, '_options'):
            self._options = {
                'debug': False
            }

    @assert_quote_init
    @lru_cache(maxsize=None, typed=True)
    def _fetch_data(self, filename, date_columns=None, iostream=None):
        """获取数据

        参数:
            filename: 数据文件名
            dtype: 字段类型
            parse_dates: 日期字段
            iostream: BytesIO 流

        返回值: DataFrame

        """

        if not iostream:
            data_file = os.path.join(self._data_path, filename)
            if not os.path.exists(data_file):
                return
            iostream = data_file

        result = None
        extname = os.path.splitext(filename)[-1][1:].lower()
        if extname == 'csv':
            if not date_columns:
                parse_dates = False
            elif type(date_columns) is list:
                parse_dates = date_columns
            elif type(date_columns) is tuple:
                parse_dates = list(date_columns)
            elif type(date_columns) is str:
                parse_dates = [date_columns]
            else:
                raise ValueError('date_columns is error.')
            result = pd.read_csv(iostream, dtype={'code': str}, parse_dates=parse_dates)
        elif extname == 'txt':
            with open(iostream, 'r') as f:
                result = f.readlines()
        return result

    @classmethod
    def _get_price_precision(cls, security) -> int:
        """获取价格精度

        参数:
            security: 字符串或列表

        返回值: 精度或精度列表

        """
        if type(security) is str:
            n = 2
            p = security.find('.')
            if p >= 0:
                code = security[:p]
                exch = security[p + 1:]
                if exch == 'SZ':
                    if code[0] == '1':
                        n = 3
                    elif code[0:3] == '399' or code[0:4] == '9000':
                        n = 4
                elif exch == 'SH':
                    if code[0] == '5':
                        n = 3
                    elif code[0:3] == '000' or code[0:4] == '1000':
                        n = 4
            return n
        elif type(security) is list:
            r = []
            for s in security:
                r.append(cls._get_price_precision(s))
            return r

    @classmethod
    def _parse_period_str(cls, period) -> (str, int):
        """分析周期字串

        参数:
            period: 周期

        返回值: 类型，间隔

        """
        if period in ['day', 'daily', '1d', 'week', '1w', 'mon', 'month', '1M', 'season', 'year']:
            period_type = 'day'
            period_step = 0
        elif period[-1] == 'm' and period[:-1].isdecimal():
            period_type = 'mn1'
            period_step = int(period[:-1])
        elif period[0:2] == 'mn' and period[2:].isdecimal():
            period_type = 'mn1'
            period_step = int(period[2:])
        else:
            raise Exception('period is invalid.')
        return period_type, period_step

    def _parse_period_start(self, period, date, count):
        """分析周期开始时间

        参数:
            period: 周期
            date: 参考时间
            count: 数量

        返回值:
            参考时间 - count 个周期后的开始时间

        """
        year_minimum = 1990
        start = datetime.datetime(2005, 1, 1).date()
        if period in ['day', 'daily', '1d']:
            trade_list = self.get_trade_days(end_date=date, count=count)
            if trade_list:
                start = trade_list[0].timetuple()
        elif period in ['week', '1w']:
            trade_list = self.get_trade_days(end_date=date, count=count * 5)
            if trade_list:
                week_maps = [x.isocalendar()[0] * 100 + x.isocalendar()[1] for x in trade_list]
                week_list = list(set(week_maps))
                week_list.sort()
                w = week_list[-count]
                start = trade_list[week_maps.index(w)].timetuple()
        elif period in ['mon', 'month', '1M']:
            y = date.tm_year
            m = date.tm_mon + 1 - count
            while m <= 0:
                y -= 1
                m += 12
            y = max(y, year_minimum)
            start = datetime.datetime(y, m, 1).timetuple()
        elif period == 'season':
            y = date.tm_year
            s = (date.tm_mon - 1) // 3 + 1 - count
            while s < 0:
                y -= 1
                s += 4
            y = max(y, year_minimum)
            start = datetime.datetime(y, s * 3 + 1, 1).timetuple()
        elif period == 'year':
            y = date.tm_year + 1 - count
            y = max(y, year_minimum)
            start = datetime.datetime(y, 1, 1).timetuple()
        else:
            t, n = self._parse_period_str(period)
            if t != 'mn1':
                return
            days = math.ceil(count * n / 240)
            trade_list = self.get_trade_days(end_date=date, count=days)
            if trade_list:
                start = trade_list[0].timetuple()
        return start

    def trace(self, *args):
        if self._options.get('debug', False):
            print(time.strftime('%Y-%m-%d %H:%M:%S'), *args)

    def get_option(self, name):
        """获取可选项值

        参数:
            name: 可选项名

        返回值:
            可选项值

        """
        if name not in self._options:
            raise ValueError('option %s is not exists.' % name)

    def set_option(self, name, value):
        """设置可选项值

        参数:
            name: 可选项名
            value: 可选项值

        """
        if name not in self._options:
            raise ValueError('option %s is not exists.' % name)
        self._options[name] = value

    def init(self, data_path):
        """初始化

        参数:
            data_path: 数据目录

        """
        if not data_path or not os.path.exists(data_path):
            raise Exception('initialization failed. data_path %s is not exists.' % data_path)
        self._data_path = data_path

    def get_data_path(self):
        """获取数据目录

        返回值: 数据目录

        """
        return self._data_path

    @assert_quote_init
    def get_quote_date(self) -> datetime.date:
        """获取行情日期

        返回值:
            最新行情日期

        """
        filename = 'ckvalid.txt'
        txt = self._fetch_data(filename)
        if not txt:
            raise Exception('fetch data from %s failed.' % filename)

        result = dict()
        for s in txt:
            s = s.strip()
            if not s:
                continue
            p = s.find('=')
            if p <= 0:
                continue
            k = s[0:p].strip()
            v = s[p + 1:].strip()
            if not k or not v:
                continue
            result[k] = v
        # self.trace(result)
        stime = result.get('last_date')
        if not stime:
            raise Exception('the quote_data not found.')
        last_date = datetime.datetime.strptime(stime, '%Y-%m-%d').date()
        tdays = self.get_trade_days(end_date=last_date, count=1)
        if not tdays:
            raise Exception('trade-days is empty.')
        return tdays[0]

    @assert_quote_init
    def get_trade_days(self, start_date=None, end_date=None, count=None) -> list:
        """获取交易日列表

        参数:
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            交易日列表；类型 [datetime.date]

        """

        start_date = formatter_st(start_date) if start_date else None
        end_date = formatter_st(end_date) if end_date else None
        dt_start = np.datetime64(
            datetime.datetime.fromtimestamp(time.mktime(start_date))) if start_date else None
        dt_end = np.datetime64(datetime.datetime.fromtimestamp(time.mktime(end_date))) if end_date else None

        filename = 'quote-tdays.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)

        result = df['date'].values
        if dt_start or dt_end or count:
            if not dt_end:
                dt_end = np.datetime64(datetime.date.today())
            if dt_start:
                result = result[np.where(result >= dt_start)]
            if dt_end:
                result = result[np.where(result <= dt_end)]
            if count and count > 0:
                result = result[-count:]
        result = [datetime.date.fromtimestamp(x.astype(datetime.datetime) / 1e9) for x in result]
        return result


    @assert_quote_init
    def get_block_info(self, block=None, types=None) -> pd.DataFrame:
        """获取板块列表

        参数:
            block: 板块代码或者板块代码的 list
            types: 板块类型；类型 字符串 list；默认值 None 获取所有板块
                   可选值: 'index', 'industry', 'concept' 等；

        返回值:
            DataFrame 对象：
                block（索引）：板块代码
                name：板块名称
                date：类型 datetime.date；行业与概念板块表示启用日期；指数板块表示最后更新日期
                type：证券类型；stock（股票）, index（指数），etf（ETF基金），fja（分级A），fjb（分级B）

        """
        block = formatter_list(block)
        types = formatter_list(types)

        filename = 'quote-block-map.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        if types:
            df = df[df['type'].isin(types)]
        if block:
            df = df[df['block'].isin(block)]
        result = df.copy()
        result.set_index('block', inplace=True)
        return result


    @assert_quote_init
    def get_industries(self) -> pd.DataFrame:
        """获取行业列表

        说明：
            本方法等同 get_block_info(types='industry')
            返回值移除索引名称，变更字段名 date 为 start_date

        """
        result = self.get_block_info(types='industry')
        result.index.name = None
        result.rename(columns={'date': 'start_date'}, inplace=True)
        return result


    @assert_quote_init
    def get_concepts(self) -> pd.DataFrame:
        """获取概念列表

        说明：
            本方法等同 get_block_info(types='concept')
            返回值移除索引名称，变更字段名 date 为 start_date

        """
        result = self.get_block_info(types='concept')
        result.index.name = None
        result.rename(columns={'date': 'start_date'}, inplace=True)
        return result


    @assert_quote_init
    def get_block_securities(self, block, types=None) -> list:
        """获取板块成份股

        参数:
            block: 板块代码，字符串
            types: 板块类型；类型 字符串 list；默认值 None
                   可选值: 'index', 'industry', 'concept' 等；

        返回值:
            证券代码列表

        """

        if not block:
            raise ValueError('block need be provided.')
        if not type(block) is str:
            raise ValueError('block is invalid.')
        types = formatter_list(types)

        filename = 'quote-block-data.csv'
        df = self._fetch_data(filename)
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        if types:
            df = df[df['type'].isin(types)]
        if block:
            df = df[df['block'] == block]
        result = df['security'].tolist()
        return result


    @assert_quote_init
    def get_index_weights(self, index_code) -> list:
        """获取指数成份股权重

        参数:
            index_code: 指数代码，字符串

        返回值:
            DataFrame 对象：
                code（索引）：证券代码
                date：更新日期
                weight：权重值
                display_name：证券名称

        """

        if not index_code:
            raise ValueError('index_code need be provided.')
        if not type(index_code) is str:
            raise ValueError('index_code is invalid.')

        filename = 'quote-block-data.csv'
        df = self._fetch_data(filename)
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        df = df[(df['block'] == index_code) & (df['type'] == 'index')]
        result = df.copy()
        result.drop(columns=['block', 'type'], inplace=True)
        result.set_index('security', inplace=True)
        result.index.name = 'code'

        df = self.get_block_info(index_code, types='index')
        date = df['date'][0] if not df.empty else None
        result.insert(0, 'date', date)

        df = self.get_security_info()
        result['display_name'] = df['display_name']
        return result


    @assert_quote_init
    def get_index_stocks(self, index_code) -> list:
        """获取指数成份股

        说明：
            本方法等同 get_block_securities(<block>, types='index')

        """
        return self.get_block_securities(index_code, types='index')


    @assert_quote_init
    def get_industry_stocks(self, industry_code) -> list:
        """获取行业成份股

        说明：
            本方法等同 get_block_securities(<block>, types='industry')

        """
        return self.get_block_securities(industry_code, types='industry')


    @assert_quote_init
    def get_concept_stocks(self, concept_code) -> list:
        """获取概念成份股

        说明：
            本方法等同 get_block_securities(<block>, types='concept')

        """
        return self.get_block_securities(concept_code, types='concept')


    @assert_quote_init
    def get_security_info(self, security=None, fields=None, types=None) -> pd.DataFrame:
        """获取证券信息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
            types: 获取证券类型；类型 字符串 list；默认值 stock；
                   可选值: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof' 等；

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                code（索引）：证券代码
                display_name：中文名称
                name：缩写简称
                start_date：上市日期；类型 datetime.date
                end_date: 退市日期；类型 datetime.date；如没有退市为 2200-01-01
                type：证券类型；stock（股票）, index（指数），etf（ETF基金），fja（分级A），fjb（分级B）

        """
        security = formatter_list(security)
        fields = formatter_list(fields)
        types = formatter_list(types, 'stock')

        result = pd.DataFrame()
        filename = 'quote-ctb.csv'
        df = self._fetch_data(filename, date_columns=('start_date', 'end_date'))
        df = df.copy()
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        if types:
            df = df[df['type'].isin(types)]
        if security:
            df = df[df['code'].isin(security)]
        if fields:
            cols_retain = ['code'] + fields
            cols_all = list(df.columns)
            cols_drop = [x for x in cols_all if x not in cols_retain]
            df.drop(columns=cols_drop, inplace=True)
        result = pd.concat([result, df], sort=False, ignore_index=True)
        result.set_index('code', inplace=True)
        return result

    @assert_quote_init
    def get_security_xrxd(self, security, start_date=None, end_date=None, count=None) -> pd.DataFrame:
        """获取证券除权除息数据

        参数:
            security: 一支股票代码或者一个股票代码的 list
            start_date: 开始日期，与 count 二选一；类型 str/struct_time/datetime.date/datetime.datetime
            end_date: 结束日期；类型 str/struct_time/datetime.date/datetime.datetime；默认值 datetime.date.today()
            count: 结果集行数，与 start_date 二选一

        返回值:
            DataFrame 对象，包含字段：
                date: 实施日期
                code：证券代码
                dividend_ratio：送股比例，每 10 股送 X 股
                transfer_ratio：转赠比例，每 10 股转增 X 股
                bonus_ratio：派息比例，每 10 股派 X 元

        """
        security = formatter_list(security)
        if not security:
            raise ValueError('security need be provided.')

        filename = 'quote-xrxd.csv'
        df = self._fetch_data(filename, date_columns='date')
        if df is None:
            raise Exception('fetch data from %s failed.' % filename)
        df = df.copy()
        df = df[df['code'].isin(security)]
        tdays = self.get_trade_days(start_date, end_date, count)
        df = df[df['date'].isin(tdays)]
        df.sort_values(['code', 'date'], axis=0, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
