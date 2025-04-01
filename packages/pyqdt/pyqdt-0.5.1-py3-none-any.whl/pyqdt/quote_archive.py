# -*- coding: utf-8 -*-
import zipfile

from io import BytesIO

import numpy as np
import pandas as pd

from .utils import *
from .quote_base import *

class QuoteArchive(QuoteBase):
    @assert_quote_init
    def get_quote_rawdata(self, date=None, fields=None, period='daily', types=None) -> pd.DataFrame:
        """获取静态行情数据

        参数:
            date: 行情日期；类型 str/struct_time/datetime.date/datetime.datetime; 默认值：最新行情日
            fields: 获取的字段；类型 字符串 list；默认值 None 获取所有字段
                   可选值：'open','close','high','low','volume','money','high_limit','low_limit','pre_close'
            period: 周期；默认值：daily；可选值：daily, minute
            types: 获取证券类型；类型 字符串 list；默认值 stock；
                   可选值: 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof' 等；

        返回值:
            DataFrame 对象，包含 fields 指定的字段：
                datetime: 行情时间
                code：证券代码
                open：开盘价
                close：收盘价
                high：最高价
                low：最低价
                volume：成交量
                money：成交额
                high_limit：涨停价
                low_limit：跌停价
                pre_close：昨日收盘价

        """
        fields = formatter_list(fields)
        types = formatter_list(types, 'stock')
        curr_date = formatter_st(date, self.get_quote_date())
        sdt = time.strftime('%Y%m%d', curr_date)

        result = pd.DataFrame()
        arc_file = os.path.join(self._data_path, sdt[:4], sdt[4:6], 'quote-data-' + sdt + '.zip')
        if not os.path.exists(arc_file):
            return result
        zf = zipfile.ZipFile(arc_file, 'r')
        for y in types:
            filename = 'quote-' + period + '-' + y + '-' + sdt + '.csv'
            if not filename in zf.namelist():
                continue
            df = self._fetch_data(filename, date_columns='time', iostream=BytesIO(zf.read(filename)))
            if df is None:
                continue
            df.rename(columns={'time': 'datetime'}, inplace=True)
            df = df.copy()
            if fields:
                cols_retain = ['datetime', 'code'] + fields
                cols_all = list(df.columns)
                cols_drop = [x for x in cols_all if x not in cols_retain]
                df.drop(columns=cols_drop, inplace=True)
            result = result.append(df, ignore_index=True)
        zf.close()

        return result