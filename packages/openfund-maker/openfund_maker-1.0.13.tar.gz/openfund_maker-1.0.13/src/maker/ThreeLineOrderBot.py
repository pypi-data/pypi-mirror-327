# -*- coding: utf-8 -*-
import time
import ccxt
import traceback
import requests
import pandas as pd

from logging.handlers import TimedRotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed


class ThreeLineOrdergBot:
    def __init__(self, config, platform_config, feishu_webhook=None,logger=None):

        self.g_config = config
        self.feishu_webhook = feishu_webhook
        self.monitor_interval = self.g_config.get("monitor_interval", 4)  # 默认值为60秒  # 监控循环时间是分仓监控的3倍
        self.trading_pairs_config = self.g_config.get('tradingPairs', {})
        self.highest_total_profit = 0  # 记录最高总盈利
        self.leverage_value = self.g_config.get('leverage', 2)
        self.is_demo_trading = self.g_config.get('is_demo_trading', 1)  # live trading: 0, demo trading: 1
        # self.instrument_info_dict = {}
        self.cross_directions = {} # 持仓期间，存储每个交易对的交叉方向 

        # 配置交易所
        self.exchange = ccxt.okx({
            'apiKey': platform_config["apiKey"],
            'secret': platform_config["secret"],
            'password': platform_config["password"],
            'timeout': 3000,
            'rateLimit': 50,
            'options': {'defaultType': 'future'},
            'proxies': {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'},
        })
        
      

        self.logger = logger
        self.position_mode = self.get_position_mode()  # 获取持仓模式

    def getMarket(self,symbol):
        self.exchange.load_markets()
        return self.exchange.market(symbol)
    
    def get_tick_size(self,symbol):
        return float(self.getMarket(symbol)['precision']['price'])
    
    # 获取价格精度
    def get_precision_length(self,symbol) -> int:
        tick_size = self.get_tick_size(symbol)
        return len(f"{tick_size:.10f}".rstrip('0').split('.')[1]) if '.' in f"{tick_size:.10f}" else 0
    
    # def decimal_to_precision(self,symbol,price) -> float:
    #     from ccxt.base.decimal_to_precision import DECIMAL_PLACES, TICK_SIZE, NO_PADDING, TRUNCATE, ROUND, ROUND_UP, ROUND_DOWN, SIGNIFICANT_DIGITS
    #     tick_size = self.get_tick_size(symbol)
    #     new_px = self.exchange.decimal_to_precision(
    #         n=float(price),
    #         precision=tick_size,
    #         rounding_mode=ROUND,
    #         counting_mode=TICK_SIZE
    #     )
        
    #     return new_px

    def get_position_mode(self):
        try:
            # 假设获取账户持仓模式的 API
            response = self.exchange.private_get_account_config()
            data = response.get('data', [])
            if data and isinstance(data, list):
                # 取列表的第一个元素（假设它是一个字典），然后获取 'posMode'
                position_mode = data[0].get('posMode', 'single')  # 默认值为单向
                self.logger.info(f"当前持仓模式: {position_mode}")
                return position_mode
            else:
                self.logger.error("无法检测持仓模式: 'data' 字段为空或格式不正确")
                return 'single'  # 返回默认值
        except Exception as e:
            self.logger.error(f"无法检测持仓模式: {e}")
            return None

    
    def fetch_and_store_all_instruments(self,instType='SWAP'):
        try:
            self.logger.info(f"Fetching all instruments for type: {instType}")
            # 获取当前交易对
            instruments = self.exchange.fetch_markets_by_type(type=instType)
            if instruments:
                # self.instrument_info_dict.clear()
                for instrument in instruments:
                    # instId = instrument['info']['instId']
                    symbol = instrument['symbol']
                    # self.instrument_info_dict[symbol] = instrument['info']
        except Exception as e:
            self.logger.error(f"Error fetching instruments: {e}")
            raise

    def send_feishu_notification(self,message):
        if self.feishu_webhook:
            headers = {'Content-Type': 'application/json'}
            data = {"msg_type": "text", "content": {"text": message}}
            response = requests.post(self.feishu_webhook, headers=headers, json=data)
            if response.status_code == 200:
                self.logger.debug("飞书通知发送成功")
            else:
                self.logger.error(f"飞书通知发送失败: {response.text}")
    # 获取K线收盘价格            
    def get_close_price(self,symbol):
        '''
        bar = 
        时间粒度，默认值1m
        如 [1m/3m/5m/15m/30m/1H/2H/4H]
        香港时间开盘价k线：[6H/12H/1D/2D/3D/1W/1M/3M]
        UTC时间开盘价k线：[/6Hutc/12Hutc/1Dutc/2Dutc/3Dutc/1Wutc/1Mutc/3Mutc]
        '''
        # response = market_api.get_candlesticks(instId=instId,bar='1m')
        klines = self.exchange.fetch_ohlcv(symbol, timeframe='1m',limit=3)
        if klines:
            # close_price = response['data'][0][4]
            # 获取前一个K线 close price
            close_price = klines[-1][4]
            return float(close_price)
        else:
            raise ValueError("Unexpected response structure or missing 'c' value")


    def get_mark_price(self,symbol):
        # response = market_api.get_ticker(instId)
        ticker = self.exchange.fetch_ticker(symbol)
        # if 'data' in response and len(response['data']) > 0:
        if ticker :
            # last_price = response['data'][0]['last']
            last_price = ticker['last']
            return float(last_price)
        else:
            raise ValueError("Unexpected response structure or missing 'last' key")

    def round_price_to_tick(self,price, tick_size):
        # 计算 tick_size 的小数位数
        tick_decimals = len(f"{tick_size:.10f}".rstrip('0').split('.')[1]) if '.' in f"{tick_size:.10f}" else 0

        # 调整价格为 tick_size 的整数倍
        adjusted_price = round(price / tick_size) * tick_size
        return f"{adjusted_price:.{tick_decimals}f}"

    def get_historical_klines(self,symbol, bar='1m', limit=241):
        # response = market_api.get_candlesticks(instId, bar=bar, limit=limit)
        params = {
            # 'instId': instId,
        }
        klines = self.exchange.fetch_ohlcv(symbol, timeframe=bar,limit=limit,params=params)
        # if 'data' in response and len(response['data']) > 0:
        if klines :
            # return response['data']
            return klines
        else:
            raise ValueError("Unexpected response structure or missing candlestick data")

    def calculate_atr(self,klines, period=60):
        trs = []
        for i in range(1, len(klines)):
            high = float(klines[i][2])
            low = float(klines[i][3])
            prev_close = float(klines[i-1][4])
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            trs.append(tr)
        atr = sum(trs[-period:]) / period
        return atr
    
    def calculate_sma_pandas(self,symbol, kLines, period) -> pd.Series:
        """
        使用 pandas 计算 SMA
        :param KLines K线
        :param period: SMA 周期
        :return: SMA 值
        """
        precision= self.get_precision_length(symbol)
        df = pd.DataFrame(kLines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        sma = df['close'].rolling(window=period).mean().round(precision)
        return sma 
               
    def calculate_ema_pandas(self,symbol, kLines, period) -> pd.Series:
        """
        使用 pandas 计算 EMA
        :param KLines K线
        :param period: EMA 周期
        :return: EMA 值
        """
        precision= self.get_precision_length(symbol)
        df = pd.DataFrame(kLines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # 计算EMA
        ema = df['close'].ewm(span=period, adjust=False).mean().round(precision)
        return ema 

    def calculate_average_amplitude(self,klines, period=60):
        amplitudes = []
        for i in range(len(klines) - period, len(klines)):
            high = float(klines[i][2])
            low = float(klines[i][3])
            close = float(klines[i][4])
            amplitude = ((high - low) / close) * 100
            amplitudes.append(amplitude)
        average_amplitude = sum(amplitudes) / len(amplitudes)
        return average_amplitude
    
    def cancel_all_orders(self,symbol):
        try:
            # 获取所有未完成订单
            params = {
                # 'instId': instId
            }
            open_orders = self.exchange.fetch_open_orders(symbol=symbol,params=params)
            
            # 取消每个订单
            for order in open_orders:
                self.exchange.cancel_order(order['id'], symbol,params=params)
                
            self.logger.info(f"{symbol} 挂单取消成功.")
        except Exception as e:
            self.logger.error(f"{symbol} 取消订单失败: {str(e)}")

    def set_leverage(self,symbol, leverage, mgnMode='isolated',posSide=None):
        try:
            # 设置杠杆
            params = {
                # 'instId': instId,
                'leverage': leverage,
                'marginMode': mgnMode
            }
            if posSide:
                params['side'] = posSide
                
            self.exchange.set_leverage(leverage, symbol=symbol, params=params)
            self.logger.debug(f"{symbol} Successfully set leverage to {leverage}x")
        except Exception as e:
            self.logger.error(f"{symbol} Error setting leverage: {e}")
    # 
    def check_position(self,symbol) -> bool:
        """
        检查指定交易对是否有持仓
        
        Args:
            symbol: 交易对ID
            
        Returns:
            bool: 是否有持仓
        """
        try:
            position = self.exchange.fetch_position(symbol=symbol)
            if position and position['contracts']> 0:
                self.logger.debug(f"{symbol} 有持仓合约数: {position['contracts']}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"{symbol} 检查持仓失败: {str(e)}")
            return False


    def place_order(self,symbol, price, amount_usdt, side):

        
        markets = self.exchange.load_markets()
        if symbol not in markets:
            self.logger.error(f"{symbol}: Instrument {symbol} not found in markets")
            return
        market = markets[symbol]
        # 获取价格精度
        price_precision = market['precision']['price']
        adjusted_price = self.round_price_to_tick(price, price_precision)

        if amount_usdt > 0:
            if side == 'buy':
                pos_side = 'long' 
            else:
                pos_side = 'short'   
            # 设置杠杆 
            self.set_leverage(symbol=symbol, leverage=self.leverage_value, mgnMode='isolated',posSide=pos_side)  
            params = {
                
                "tdMode": 'isolated',
                "side": side,
                "ordType": 'limit',
                # "sz": amount_usdt,
                "px": str(adjusted_price)
            } 
            
            # 模拟盘(demo_trading)需要 posSide
            if self.is_demo_trading == 1 :
                params["posSide"] = pos_side
                
            # self.logger.debug(f"---- Order placed params: {params}")
            try:
                order = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'limit',
                    'amount': amount_usdt,
                    'price': float(adjusted_price),
                    'params': params
                }
                # 使用ccxt创建订单
                self.logger.debug(f"Pre Order placed:  {order} ")
                order_result = self.exchange.create_order(
                    **order
                    # symbol=symbol,
                    # type='limit',
                    # side=side,
                    # amount=amount_usdt,
                    # price=float(adjusted_price),
                    # params=params
                )
                # self.logger.debug(f"{symbol} ++ Order placed rs :  {order_result}")
            except Exception as e:
                self.logger.error(f"{symbol} Failed to place order: {e}")
        self.logger.info(f"--------- ++ {symbol} Order placed done! --------")   
        
    # 定义根据均线斜率判断 K 线方向的函数： 0 空 1 多 -1 平
    def judge_k_line_direction(self,symbol, pair_config, ema:pd.Series) -> int:
        """
        判断K线方向
        Args:
            symbol: 交易对
            pair_config: 配置参数
            ema: EMA数据
        Returns:
            int: -1:平, 0:空, 1:多
        """
        def check_ema_range(ema_data: pd.Series, period: int, limit: float, tick_size: float) -> bool:
            """检查EMA是否在指定范围内震荡"""
            ema_window = ema_data[-period:]
            price_range = ema_window.max() - ema_window.min()
            return abs(price_range) <= limit * tick_size
            
        def get_trend_direction(slope: float) -> int:
            """根据斜率判断趋势方向"""
            if slope > 0:
                return 1    # 上升趋势
            elif slope < 0:
                return 0    # 下降趋势
            return -1       # 震荡趋势
            
        # 获取配置参数
        tick_size = self.get_tick_size(symbol)
        ema_range_period = int(pair_config.get('ema_range_period', 3))
        ema_range_limit = float(pair_config.get('ema_range_limit', 1))
        
        # 判断是否在震荡区间
        if check_ema_range(ema, ema_range_period, ema_range_limit, tick_size):
            direction = -1
        else:
            # 计算最新斜率并判断方向
            latest_slope = ema.diff().iloc[-1]
            direction = get_trend_direction(latest_slope)
            
        self.logger.debug(f"{symbol}: 极差={abs(ema[-ema_range_period:].max() - ema[-ema_range_period:].min()):.9f} "
                         f"斜率={ema.diff().iloc[-1]:.9f}, K线方向 {direction}")
        
        return direction
  
    def judge_cross_direction(self,fastklines,slowklines) :
        # 创建DataFrame
        df = pd.DataFrame({
            'fast': fastklines,
            'slow': slowklines
        })
        
        # 判断金叉和死叉
        df['golden_cross'] = (df['fast'] > df['slow']) & (df['fast'].shift(1) < df['slow'].shift(1))
        df['death_cross'] = (df['fast'] < df['slow']) & (df['fast'].shift(1) > df['slow'].shift(1))
        
        # 从后往前找最近的交叉点
        last_golden = df['golden_cross'].iloc[::-1].idxmax() if df['golden_cross'].any() else None
        last_death = df['death_cross'].iloc[::-1].idxmax() if df['death_cross'].any() else None
        
        # 判断最近的交叉类型
        if last_golden is None and last_death is None:
            return {
                'cross': -1,  # 无交叉
                'index': None
            }
        
        # 如果金叉更近或只有金叉
        if last_golden is not None and (last_death is None or last_golden > last_death):
            return {
                'cross': 1,  # 金叉
                'index': last_golden
            }
        # 如果死叉更近或只有死叉
        else:
            return {
                'cross': 0,  # 死叉
                'index': last_death
            }
        
    def judge_ma_apex(self,symbol, fastklines,slowklines) -> bool:

        df = pd.DataFrame({
            'ema': fastklines,
            'sma': slowklines
        })
        # 快线和慢线的差值
        # 将ema和sma转换为tick_size精度
        # df['diff'] = df['ema'].apply(lambda x: float(self.round_price_to_tick(x, tick_size))) - df['sma'].apply(lambda x: float(self.round_price_to_tick(x, tick_size)))
        df['diff'] = df['ema']-df['sma']
        # 计算斜率，【正】表示两线距离扩张，【负】表示两线距离收缩
        df['slope'] = df['diff'].abs().diff().round(4)
        df['flag'] = df['slope'] <= 0.0
        
        self.logger.debug(f"{symbol}: slopes = \n{df[['ema','sma','diff','slope','flag']].iloc[-6:-1]}  ")
        # 检查最后两个斜率是否都为负
        # 取slopes最新的第2个和第3个值进行判断
        
        return all(slope <= 0.0 for slope in df['slope'].iloc[-3:-1])
        
        
    def calculate_range_diff(self,prices:pd.Series) -> float:
        """
        计算价格列表中最后一个价格与第一个价格的差值。
        Args:
            prices: 价格列表。
        Returns:
            diff: 计算最高价列的最大值与最小值的差值
。
        """
        if prices.empty:
            return None
        # 将价格列表转换为pandas Series格式
  
        diff = prices.max() - prices.min()
        
        return diff
    
    def calculate_place_order_price(self, symbol,side,base_price, amplitude_limit, offset=1) -> float:
        """
        计算开仓价格
        Args:
            symbol: 交易对
            side: 开仓方向
            base_price: 开盘价格
            amplitude_limit: 振幅限制
            offset: 偏移量
        Returns:
            place_order_price: 开仓价格
        """
        tick_size = float(self.exchange.market(symbol)['precision']['price'])
        place_order_price = None
        # 计算止盈价格，用市场价格（取持仓期间历史最高）减去开仓价格的利润，再乘以不同阶段的止盈百分比。
      
        if side == 'buy':
            place_order_price = base_price * (1- amplitude_limit/100) - offset * tick_size
        else:
            place_order_price = base_price * (1 + amplitude_limit/100) + offset * tick_size
        self.logger.debug(f"++++ {symbol} 下单价格: {place_order_price:.9f} 方向 {side} 基准价格{base_price} 振幅限制 {amplitude_limit} ")
        return float(self.round_price_to_tick(place_order_price,tick_size))
      
    def process_pair(self,symbol,pair_config):
        # 检查是否有持仓，有持仓不进行下单
        if self.check_position(symbol=symbol) :
            self.logger.info(f"{symbol} 有持仓合约，不进行下单。")
            return 
        # 取消之前的挂单
        self.cancel_all_orders(symbol=symbol)  
           
        try:
            klines = self.get_historical_klines(symbol=symbol)
            # 提取收盘价数据用于计算 EMA
            # 从K线数据中提取收盘价，按时间顺序排列（新数据在后）
            # close_prices = [float(kline[4]) for kline in klines]
            is_bullish_trend = False
            is_bearish_trend = False

            # 计算 快线EMA & 慢线SMA
            ema_length = pair_config.get('ema', 15)
            sma_length = pair_config.get('sma', 50)
            
            # 增加 金叉死叉 方向确认的 20250209
            fastk = self.calculate_ema_pandas(symbol, klines, period=ema_length)
            slowk = self.calculate_sma_pandas(symbol, klines, period=sma_length)

            cross_direction = self.judge_cross_direction(fastklines=fastk,slowklines=slowk)
            # 更新交叉状态
            if cross_direction['cross'] != -1 :  #本次不一定有交叉
                self.cross_directions[symbol] = cross_direction
            
            # 最新交叉方向
            last_cross_direction = self.exchange.safe_dict(self.cross_directions,symbol,None)
                
                
            # 判断趋势：多头趋势或空头趋势
            direction = self.judge_k_line_direction(symbol=symbol, pair_config=pair_config,ema=fastk) 
            if direction == 1:
                is_bullish_trend = True     
            elif direction == 0:
                is_bearish_trend = True
     
            # 结合金叉死叉判断是否是周期顶部和底部
            is_apex = self.judge_ma_apex(symbol=symbol,fastklines=fastk,slowklines=slowk)
            # 金叉死叉逻辑
            if last_cross_direction and last_cross_direction['cross'] == 1 : # 金叉
                self.logger.debug(f"{symbol} 金叉:{last_cross_direction}，清理空单，挂多单！！")
                is_bearish_trend = False
                if is_apex :
                    self.logger.debug(f"{symbol} 金叉:{last_cross_direction}，周期见顶 {is_apex}，不开单！！")
                    is_bullish_trend = False
                    
            elif last_cross_direction and last_cross_direction['cross'] == 0 : # 死叉
                self.logger.debug(f"{symbol} 死叉:{last_cross_direction}，清理多单，挂空单！！")
                is_bullish_trend = False  
                if is_apex :
                    self.logger.debug(f"{symbol} 死叉:{last_cross_direction}，周期见顶 {is_apex}，不开单！！")
                    is_bearish_trend = False
                    
            else:
                self.logger.debug(f"{symbol} 当前没有金叉死叉，以快线趋势为准。！")
                   
            
            if  (not is_bullish_trend and not is_bearish_trend) or  direction == -1 :
                self.logger.info(f"{symbol} 当前是震荡趋势（平），不挂单！！direction={direction}")
                return  

            '''
            取当前K线的前三根K线中最高/低的值作为止盈位。
            20250210 增加开单价格约束，下单时，三线如果价格振幅小（如0.32%内），那去找到0.32%外的那根。 振幅 amplitude_limit
            '''    
            
            # 取当前 K 线的前三根 K 线
      
            df_3 = pd.DataFrame(klines[-4:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            low_prices = df_3['low']
            high_prices = df_3['high']
            max_high = high_prices.max()
            min_low = low_prices.min()
      
            # 计算当前 振幅是否超过amplitude_limit
            
            amplitude_limit = pair_config.get('amplitude_limit', 0.32)
            
            self.logger.debug(f"{symbol} 当前K线的前三根K线 最高价: {max_high}, 最低价: {min_low}")
  
     
            
            long_amount_usdt = pair_config.get('long_amount_usdt', 5)
            short_amount_usdt = pair_config.get('short_amount_usdt', 5)     
                            
            '''
            挂单线都是三线中最高/低，如果打到下单线说明趋势反转，所以应该挂和反方向的单，
            
            '''
            # 取最新K线的收盘价格
            close_price = klines[-1][4]
            self.logger.debug(f"-- {symbol} 最新K线 {klines[-1]}")
            
            if is_bullish_trend:
                diff = self.calculate_range_diff(prices=low_prices)
                cur_amplitude_limit =  diff / close_price * 100 
                self.logger.info(f"{symbol} 当前为上升（多）趋势，允许挂多单，振幅{cur_amplitude_limit:.3f} hight/low {low_prices.max()}/{low_prices.min()} ++")
                # 振幅大于限制，直接下单,否则，根据振幅计算下单价格
                if  cur_amplitude_limit >= amplitude_limit:
                    self.place_order(symbol, min_low, long_amount_usdt, 'buy')
                else:
                    entry_price = self.calculate_place_order_price(symbol,side='buy',base_price=min_low, amplitude_limit=amplitude_limit,offset=0)
                    self.place_order(symbol, entry_price ,long_amount_usdt, 'buy')
                   

            if is_bearish_trend:
                diff = self.calculate_range_diff(prices=high_prices)
                cur_amplitude_limit =  diff / close_price * 100 
                self.logger.info(f"{symbol} 当前为下降（空）趋势，允许挂空单，振幅{cur_amplitude_limit:.3f} hight/low {high_prices.max()}/{high_prices.min()}--")
                if cur_amplitude_limit >= amplitude_limit:
                    self.place_order(symbol, max_high, short_amount_usdt, 'sell')
                else:
                    entry_price = self.calculate_place_order_price(symbol,side='sell',base_price=max_high, amplitude_limit=amplitude_limit,offset=0)
                    self.place_order(symbol, entry_price ,long_amount_usdt, 'sell')  

        except KeyboardInterrupt:
            self.logger.info("程序收到中断信号，开始退出...")
        except Exception as e:
            error_message = f"程序异常退出: {str(e)}"
            self.logger.error(error_message,exc_info=True)
            traceback.print_exc()
            self.send_feishu_notification(error_message)


            
    def monitor_klines(self):
        symbols = list(self.trading_pairs_config.keys())  # 获取所有币对的ID
        batch_size = 5  # 每批处理的数量
        while True:

            for i in range(0, len(symbols), batch_size):
                batch = symbols[i:i + batch_size]
                with ThreadPoolExecutor(max_workers=batch_size) as executor:
                    futures = [executor.submit(self.process_pair, symbol,self.trading_pairs_config[symbol]) for symbol in batch]
                    for future in as_completed(futures):
                        future.result()  # Raise any exceptions caught during execution

            time.sleep(self.monitor_interval)