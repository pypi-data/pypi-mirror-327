"""
商品模块数据采集
"""

from random import uniform
from time import sleep, time

from DrissionPage import Chromium

from .._utils import Utils
from ._dict import Dictionary
from ._utils import parse__localstorage_data


class Urls:
    goods360 = 'https://sycm.taobao.com/cc/item_archives'
    goods360__sale = 'https://sycm.taobao.com/cc/item_archives?activeKey=sale&dateRange={begin_date}%7C{end_date}&dateType=day&itemId={goods_id}'
    goods360__flow = 'https://sycm.taobao.com/cc/item_archives?activeKey=flow&dateRange={begin_date}%7C{end_date}&dateType=day&itemId={goods_id}'


class DataPacketUrls:
    goods360__browser_history = 'sycm.taobao.com/cc/item/browseHistory.json'
    """商品360-历史浏览商品列表"""
    goods360__sale__overview = 'sycm.taobao.com/cc/item/sale/overview.json'
    """商品360-销售分析概览"""
    goods360__goods_info = 'sycm.taobao.com/cc/item/crowd/info.json'
    """商品360-指定商品信息"""
    goods360__flow__detail = 'sycm.taobao.com/flow/v6/item/crowdtype/source/v3.json'
    """商品360-流量来源详情"""


class Goods:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def get__goods360__sale__overview(
        self, goods_ids: list[str], date: str, raw=False, timeout: float = None
    ):
        """
        获取商品360-销售分析数据概览

        Returns:
            数据列表 {商品ID: {字段, 值}, ...}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods360__browser_history,
            method='GET',
            res_type='Fetch',
        )
        page.get(Urls.goods360)
        browser_history_packet = page.listen.wait(timeout=_timeout)
        if not browser_history_packet:
            raise TimeoutError('进入商品360获取历史浏览商品列表数据超时')

        query_token = browser_history_packet.request.params.get('token')

        page.change_mode('s', go=False)

        def query_api(goods_id: str):
            """通过API查询数据"""

            print(f'[{goods_id}] 通过 API 查询商品销售分析数据概览')

            query_data = {
                'dateType': 'day',
                'dateRange': f'{date}|{date}',
                'device': 0,
                'itemId': goods_id,
                '_': int(time() * 1000),
                'token': query_token,
            }
            api_url = f'https://{DataPacketUrls.goods360__sale__overview}'
            headers = {
                'referer': Urls.goods360__sale.format(
                    begin_date=date, end_date=date, goods_id=goods_id
                )
            }
            if not page.get(
                api_url, params=query_data, headers=headers, timeout=_timeout
            ):
                print('- API 请求失败')
                return

            if (status_code := page.response.status_code) != 200:
                print(f'- API 请求失败，状态码：{status_code}')
                return

            response = page.response.json()
            if not isinstance(response, dict):
                print('- 返回的数据包格式非预期 dict 类型')
                return

            if 'data' not in response:
                print('- 返回的数据包中无 data 字段')
                return
            data = response['data']
            if not isinstance(data, dict):
                print('- 返回的数据包中 data 字段格式非预期 dict 类型')
                return

            return data

        data_list: dict[str, dict] = {}
        for goods_id in goods_ids:
            data = query_api(goods_id)
            sleep(uniform(2.2, 3.2))
            if not data:
                continue

            data_list[goods_id] = data

        page.change_mode('d', go=False)
        page.close()

        if not data_list:
            return

        if raw is True:
            return data_list

        records: dict[str, dict] = {}
        for goods_id, data in data_list.items():
            record = Utils.dict_mapping(data, Dictionary.goods.goods360__sale__overview)
            record = {k: v['value'] for k, v in record.items()}

            record = Utils.dict_format__ratio(
                record,
                fields=[
                    '商品详情页跳出率',
                    '访问收藏转化率',
                    '访问加购转化率',
                    '下单转化率',
                    '支付转化率',
                ],
            )
            record = Utils.dict_format__round(record)

            records[goods_id] = record

        return records

    def get__goods360__goods_info(
        self, goods_ids: list[str], raw=False, timeout: float = None
    ):
        """
        通过商品360获取商品信息
        - 例如商品的标题
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods360__browser_history,
            method='GET',
            res_type='Fetch',
        )
        page.get(Urls.goods360)
        browser_history_packet = page.listen.wait(timeout=_timeout)
        if not browser_history_packet:
            raise TimeoutError('进入商品360获取历史浏览商品列表数据超时')

        query_token = browser_history_packet.request.params.get('token')

        yesterday = Utils.date_yesterday()

        page.change_mode('s', go=False)

        def query_api(goods_id: str):
            """通过API查询数据"""
            print(f'[{goods_id}] 通过 API 查询商品信息')

            query_data = {
                'dateType': 'day',
                'dateRange': f'{yesterday}|{yesterday}',
                'itemId': goods_id,
                '_': int(time() * 1000),
                'token': query_token,
            }
            api_url = f'https://{DataPacketUrls.goods360__goods_info}'
            headers = {
                'referer': Urls.goods360__sale.format(
                    begin_date=yesterday, end_date=yesterday, goods_id=goods_id
                )
            }
            if not page.get(
                api_url, params=query_data, headers=headers, timeout=_timeout
            ):
                print('- API 请求失败')
                return

            if (status_code := page.response.status_code) != 200:
                print(f'- API 请求失败，状态码：{status_code}')
                return

            response = page.response.json()
            if not isinstance(response, dict):
                print('- 返回的数据包格式非预期 dict 类型')
                return

            if 'data' not in response:
                print('- 返回的数据包中无 data 字段')
                return

            data = response['data']
            if not isinstance(data, dict):
                print('- 返回的数据包中 data 字段格式非预期 dict 类型')
                return

            return data

        data_list: dict[str, dict] = {}
        for goods_id in goods_ids:
            data = query_api(goods_id)
            sleep(uniform(2.2, 3.2))
            if not data:
                continue

            data_list[goods_id] = data

        page.change_mode('d', go=False)
        page.close()

        if not data_list:
            return

        if raw is True:
            return data_list

        records: dict[str, dict] = {}
        for goods_id, data in data_list.items():
            record = Utils.dict_mapping(data, Dictionary.goods.goods360__goods_info)
            records[goods_id] = record

        return records

    def get__goods360__sale__overview__normal(
        self, goods_id: str, date: str, raw=False, timeout: float = None
    ):
        """获取商品360-销售分析数据概览 (通过页面正常访问)"""

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods360__sale__overview,
            method='GET',
            res_type='Fetch',
        )
        uri = Urls.goods360__sale.format(
            begin_date=date, end_date=date, goods_id=goods_id
        )
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)

        data: dict = None
        if not packet:
            # 如果数据包获取超时则通过 localStorage 获取数据
            local_storage: dict = page.local_storage()
            for key, value in local_storage.items():
                if (
                    DataPacketUrls.goods360__sale__overview in key
                    and f'{date}|{date}' in key
                    and goods_id in key
                ):
                    data = parse__localstorage_data(value)
                    break
        else:
            response = packet.response.body
            if not isinstance(response, dict):
                raise ValueError('返回的数据包格式非预期 dict 类型')

            if 'data' not in response:
                raise ValueError('返回的数据包中未找到 data 字段')

            _data = response['data']
            if not isinstance(_data, dict):
                raise ValueError('返回的数据包中 data 字段格式非预期 dict 类型')

            data = _data

        if not data:
            raise RuntimeError('数据包及本地均未获取到数据')

        # ========== 获取商品标题 ==========
        title_ele = page.ele('c:div.item-header strong', timeout=3)
        title = None
        if title_ele:
            title = title_ele.attr('title')
        # ========== 获取商品标题 ==========

        page.close()

        if raw is True:
            return data

        record = Utils.dict_mapping(data, Dictionary.goods.goods360__sale__overview)
        record = {k: v['value'] for k, v in record.items()}

        record = Utils.dict_format__ratio(
            record,
            fields=[
                '商品详情页跳出率',
                '访问收藏转化率',
                '访问加购转化率',
                '下单转化率',
                '支付转化率',
            ],
        )
        record = Utils.dict_format__round(record)
        record['商品标题'] = title

        return record

    def get__goods360__flow__detail(
        self,
        goods_ids: list[str],
        module_names: list[str],
        date: str,
        raw=False,
        timeout: float = None,
    ):
        """
        获取商品360-流量来源数据详情 (旧版)

        Args:
            module_names: 模块名称列表, 例如效果广告/站外广告
        Returns:
            数据列表 {商品ID: {模块名称: {字段, 值}, ...}, ...}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods360__browser_history,
            method='GET',
            res_type='Fetch',
        )
        page.get(Urls.goods360)
        browser_history_packet = page.listen.wait(timeout=_timeout)
        if not browser_history_packet:
            raise TimeoutError('进入商品360获取历史浏览商品列表数据超时')

        query_token = browser_history_packet.request.params.get('token')

        page.change_mode('s', go=False)

        def query_api(goods_id: str):
            """通过API查询数据"""

            print(f'[{goods_id}] 通过 API 查询商品流量来源详情')

            query_data = {
                'belong': 'all',
                'dateRange': f'{date}|{date}',
                'dateType': 'day',
                'pageSize': 10,
                'page': 1,
                'order': 'desc',
                'orderBy': 'uv',
                'itemId': goods_id,
                'device': 2,
                'indexCode': 'uv,cartByrCnt,payByrCnt',
                '_': int(time() * 1000),
                'token': query_token,
            }
            api_url = f'https://{DataPacketUrls.goods360__flow__detail}'
            headers = {
                'referer': Urls.goods360__flow.format(
                    begin_date=date, end_date=date, goods_id=goods_id
                )
            }
            if not page.get(
                api_url, params=query_data, headers=headers, timeout=_timeout
            ):
                print('- API 请求失败')
                return

            if (status_code := page.response.status_code) != 200:
                print(f'- API 请求失败，状态码：{status_code}')
                return

            response = page.response.json()
            if not isinstance(response, dict):
                print('- 返回的数据包格式非预期 dict 类型')
                return

            if 'data' not in response:
                print('- 返回的数据包中无 data 字段')
                return

            data: list[dict] = response['data']
            if not isinstance(data, list):
                print('- 返回的数据包中 data 字段格式非预期 list 类型')
                return

            return data

        data_list: dict[str, dict] = {}
        for goods_id in goods_ids:
            data = query_api(goods_id)
            sleep(uniform(2.2, 3.2))
            if not data:
                continue

            data = {
                x['pageName']['value']: x
                for x in data
                if x['pageName']['value'] in module_names
            }

            data_list[goods_id] = data

        page.change_mode('d', go=False)
        page.close()

        if not data_list:
            return

        if raw is True:
            return data_list

        records: dict[str, dict] = {}
        for goods_id, data in data_list.items():
            record: dict[str, dict] = {}
            for module_name, module_data in data.items():
                _module_data = Utils.dict_mapping(
                    module_data, Dictionary.goods.goods360__flow__detail
                )
                _module_data = {k: v['value'] for k, v in _module_data.items()}
                _module_data = Utils.dict_format__ratio(
                    _module_data, fields=['下单转化率', '支付转化率']
                )
                _module_data = Utils.dict_format__round(_module_data)

                record[module_name] = _module_data

            records[goods_id] = record

        return records

    def get__goods360__flow__detail__normal(
        self,
        goods_id: str,
        module_names: list[str],
        date: str,
        raw=False,
        timeout: float = None,
    ):
        """
        获取商品360-流量来源数据详情 (旧版,通过页面正常访问)

        Args:
            module_names: 模块名称列表, 例如效果广告/站外广告
        Returns:
            数据列表 {{模块名称: {字段, 值}, ...}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods360__flow__detail,
            method='GET',
            res_type='Fetch',
        )
        uri = Urls.goods360__flow.format(
            begin_date=date, end_date=date, goods_id=goods_id
        )
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)

        data: list[dict] = None
        if not packet:
            # 如果数据包获取超时则通过 localStorage 获取数据
            local_storage: dict = page.local_storage()
            for key, value in local_storage.items():
                if (
                    DataPacketUrls.goods360__flow__detail in key
                    and f'{date}|{date}' in key
                    and goods_id in key
                ):
                    data = parse__localstorage_data(value)
                    break
        else:
            response = page.response.json()
            if not isinstance(response, dict):
                raise ValueError('返回的数据包格式非预期 dict 类型')

            if 'data' not in response:
                raise ValueError('返回的数据包中无 data 字段')

            data: list[dict] = response['data']
            if not isinstance(data, list):
                raise ValueError('返回的数据包中 data 字段格式非预期 list 类型')

        page.close()

        if not data:
            raise RuntimeError('数据包及本地均未获取到数据')

        data: dict[str, dict] = {
            x['pageName']['value']: x
            for x in data
            if x['pageName']['value'] in module_names
        }

        if raw is True:
            return data

        records: dict[str, dict] = {}
        for module_name, module_data in data.items():
            _module_data = Utils.dict_mapping(
                module_data, Dictionary.goods.goods360__flow__detail
            )
            _module_data = {k: v['value'] for k, v in _module_data.items()}
            _module_data = Utils.dict_format__ratio(
                _module_data, fields=['下单转化率', '支付转化率']
            )
            _module_data = Utils.dict_format__round(_module_data)

            records[module_name] = _module_data

        return records
