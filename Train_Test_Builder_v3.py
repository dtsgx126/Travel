"""
SGX限价订单簿高频交易策略 - 训练测试数据构建模块 (Python 3版本)

本模块负责从订单簿快照数据中提取特征并构建训练测试数据集。
主要功能:
1. 读取订单簿CSV文件
2. 计算30种不同时间窗口的价格涨跌比率特征
3. 计算17种不同权重组合的订单簿深度特征
4. 生成交易标签(未来是否可交易)
5. 输出上午和下午两个时段的特征数据框

作者: 升级至Python 3.8+
日期: 2024年
依赖: pandas>=1.5.0, numpy>=1.23.0
"""

import numpy as np
import pandas as pd
import os


def order_book(month, day, data_path='./'):
    """
    读取订单簿CSV文件并提取买卖盘数据
    
    参数:
        month: 月份
        day: 日期
        data_path: 数据文件路径
    
    返回:
        timestamp: 时间戳数组
        order_book: 完整订单簿DataFrame
        bid_price_1, bid_price_2, bid_price_3: 买盘前三档价格
        bid_quantity_1, bid_quantity_2, bid_quantity_3: 买盘前三档数量
        ask_price_1, ask_price_2, ask_price_3: 卖盘前三档价格
        ask_quantity_1, ask_quantity_2, ask_quantity_3: 卖盘前三档数量
    """
    datapath = os.path.join(data_path, f'order_book_3_2014_{month}_{day}.csv')
    order_book = pd.read_csv(datapath, sep=',')
    
    # 提取买盘数据 (每4行一组,第1-3行是价格和数量)
    bid_price_1 = np.array(list(map(float, order_book['Bid'][1::4]))) / 100.0
    bid_price_2 = np.array(list(map(float, order_book['Bid'][2::4]))) / 100.0
    bid_price_3 = np.array(list(map(float, order_book['Bid'][3::4]))) / 100.0
    
    # 提取时间戳 (每4行第0行是时间戳)
    timestamp = np.array(order_book['Bid_Quantity'][0::4])
    
    # 提取买盘数量
    bid_quantity_1 = np.array(list(map(float, order_book['Bid_Quantity'][1::4])))
    bid_quantity_2 = np.array(list(map(float, order_book['Bid_Quantity'][2::4])))
    bid_quantity_3 = np.array(list(map(float, order_book['Bid_Quantity'][3::4])))
    
    # 提取卖盘数据
    ask_price_1 = np.array(list(map(float, order_book['Ask'][1::4]))) / 100.0
    ask_price_2 = np.array(list(map(float, order_book['Ask'][2::4]))) / 100.0
    ask_price_3 = np.array(list(map(float, order_book['Ask'][3::4]))) / 100.0
    
    # 提取卖盘数量
    ask_quantity_1 = np.array(list(map(float, order_book['Ask_Quantity'][1::4])))
    ask_quantity_2 = np.array(list(map(float, order_book['Ask_Quantity'][2::4])))
    ask_quantity_3 = np.array(list(map(float, order_book['Ask_Quantity'][3::4])))
    
    # 处理NaN值,替换为0
    bid_quantity_1[np.isnan(bid_quantity_1)] = 0
    bid_quantity_2[np.isnan(bid_quantity_2)] = 0
    bid_quantity_3[np.isnan(bid_quantity_3)] = 0
    ask_quantity_1[np.isnan(ask_quantity_1)] = 0
    ask_quantity_2[np.isnan(ask_quantity_2)] = 0
    ask_quantity_3[np.isnan(ask_quantity_3)] = 0
    
    return (timestamp, order_book, bid_price_1, bid_price_2, bid_price_3, 
            bid_quantity_1, bid_quantity_2, bid_quantity_3,
            ask_price_1, ask_price_2, ask_price_3, 
            ask_quantity_1, ask_quantity_2, ask_quantity_3)


def time_transform(timestamp_time):
    """
    将时间戳字符串转换为秒数
    
    参数:
        timestamp_time: 时间戳字符串数组
    
    返回:
        time_second: 绝对秒数数组
        time_second_basic: 相对于09:00的秒数数组
    """
    time_second_basic = []
    time_second = []
    
    for i in range(len(timestamp_time)):
        # 解析时间戳: "2014-01-02D09:00:00.123456"
        # 计算总秒数
        second = (float(timestamp_time[i][11]) * 36000 + 
                 float(timestamp_time[i][12]) * 3600 +
                 float(timestamp_time[i][14]) * 600 + 
                 float(timestamp_time[i][15]) * 60 +
                 float(timestamp_time[i][17]) * 10 + 
                 float(timestamp_time[i][18]))
        
        # 减去09:00:00的秒数(32400秒)得到相对秒数
        time_second_basic.append(second - 32400.0)
        time_second.append(second)
    
    return np.array(time_second), np.array(time_second_basic)


def weight_percentage(w1, w2, w3, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                      bid_quantity_1, bid_quantity_2, bid_quantity_3):
    """
    计算加权订单簿深度特征
    
    参数:
        w1, w2, w3: 三档价格的权重
        ask_quantity_1/2/3: 卖盘三档数量
        bid_quantity_1/2/3: 买盘三档数量
    
    返回:
        W_AB: 加权卖盘数量 / 加权买盘数量
        W_A_B: (加权卖盘数量 - 加权买盘数量) / (加权卖盘数量 + 加权买盘数量)
    """
    # 计算加权数量
    Weight_Ask = w1 * ask_quantity_1 + w2 * ask_quantity_2 + w3 * ask_quantity_3
    Weight_Bid = w1 * bid_quantity_1 + w2 * bid_quantity_2 + w3 * bid_quantity_3
    
    # 计算比率特征和差值特征
    W_AB = Weight_Ask / Weight_Bid
    W_A_B = (Weight_Ask - Weight_Bid) / (Weight_Ask + Weight_Bid)
    
    return W_AB, W_A_B


def rise_ask(Ask1, timestamp_time_second, before_time):
    """
    计算卖一价的涨跌比率
    
    参数:
        Ask1: 卖一价数组
        timestamp_time_second: 时间戳秒数数组
        before_time: 回溯时间窗口(秒)
    
    返回:
        rise_ratio: 涨跌比率数组(百分比)
    
    算法说明:
        对于每个时间点,计算当前价格相对于before_time秒前价格的涨跌百分比
        公式: (当前价 - 基准价) / 基准价 * 100
    """
    # 处理0值,替换为平均价格
    Ask1[Ask1 == 0] = np.mean(Ask1)
    rise_ratio = []
    
    # 找到第一个满足时间窗口的索引
    index = np.where(timestamp_time_second >= before_time)[0][0]
    
    # 处理前before_time秒的数据,相对于开盘价计算
    for i in range(index):
        rise_ratio_ = round((Ask1[i] - Ask1[0]) / Ask1[0] * 100, 5)
        rise_ratio.append(rise_ratio_)
    
    # 处理后续数据,相对于before_time秒前的价格计算
    for i in range(index, len(Ask1)):
        index_start = np.where(timestamp_time_second[:i] >= timestamp_time_second[i] - before_time)[0][0]
        rise_ratio_ = round((Ask1[i] - Ask1[index_start]) / Ask1[index_start] * 100, 5)
        rise_ratio.append(rise_ratio_)
    
    return np.array(rise_ratio)


def traded_label_one_second(time1, time2, time_second_basic, bid_price_1, ask_price_1, traded_time,
                            rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
                            rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
                            rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
                            rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
                            rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
                            rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
                            rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
                            rise_ratio_ask_29, rise_ratio_ask_30,
                            W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001, 
                            W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
                            W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721, 
                            W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190, 
                            W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460, 
                            W_AB_127, W_A_B_127, W_AB_235, W_A_B_235):
    """
    生成交易标签和特征数据
    
    参数:
        time1, time2: 时间段起止(相对于09:00的秒数)
        time_second_basic: 时间戳秒数数组
        bid_price_1, ask_price_1: 买一价和卖一价
        traded_time: 预测时间窗口(秒)
        rise_ratio_ask_1~30: 30个涨跌比率特征
        W_AB_*, W_A_B_*: 34个深度特征
    
    返回:
        traded: 交易标签数组 (1=可交易, 0=不可交易)
        index_: 起止索引
        rise_ratio_second_1~30: 每秒的涨跌比率特征
        w_divid_*, w_diff_*: 每秒的深度特征
    """
    # 初始化返回列表
    traded = []
    index_ = []
    
    # 初始化30个涨跌比率特征列表
    rise_ratio_second = [[] for _ in range(30)]
    
    # 初始化34个深度特征列表
    w_divid = {
        '100': [], '010': [], '001': [], '910': [], '820': [], '730': [],
        '640': [], '550': [], '721': [], '532': [], '111': [], '190': [],
        '280': [], '370': [], '460': [], '127': [], '235': []
    }
    w_diff = {
        '100': [], '010': [], '001': [], '910': [], '820': [], '730': [],
        '640': [], '550': [], '721': [], '532': [], '111': [], '190': [],
        '280': [], '370': [], '460': [], '127': [], '235': []
    }
    
    # 找到时段起始点索引
    if time1 == 0:
        index_one = np.where(time_second_basic <= 0)[0][-1]
    elif time1 == 14400:
        index_one = np.where(time_second_basic <= 14400)[0][-1]
    
    # 遍历时间段内每一秒
    for i in range(time1, time2):
        if i == 0 or i == 14400:
            index_array = np.where(time_second_basic <= i)[-1]
        else:
            index_array = np.where((time_second_basic < i + 1) & (time_second_basic >= i))[-1]
        
        if len(index_array) > 0:
            # 当前秒有数据
            index = index_array[-1]
            
            # 记录起止索引
            if i == time1:
                index_.append(index)
            if i == time2 - 1:
                index_.append(index)
            
            # 生成交易标签
            if i < 25200 - traded_time:
                # 查看未来traded_time秒内的价格
                index_min = np.where(time_second_basic <= i + traded_time)[0][-1]
                traded_min = ask_price_1[index:index_min]
                
                # 如果当前买一价高于未来最低卖一价,则可以交易
                if bid_price_1[index] > np.min(traded_min):
                    traded.append(1)
                else:
                    traded.append(0)
            else:
                # 临近收盘,只能与收盘价比较
                if bid_price_1[index] > ask_price_1[-1]:
                    traded.append(1)
                else:
                    traded.append(0)
            
            # 提取当前时刻的特征值
            offset = index - index_one
            
            # 涨跌比率特征
            for j in range(30):
                rise_ratio_vars = [rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
                                  rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
                                  rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
                                  rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
                                  rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
                                  rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
                                  rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
                                  rise_ratio_ask_29, rise_ratio_ask_30]
                rise_ratio_second[j].append(rise_ratio_vars[j][offset])
            
            # 深度特征
            idx = index_one + offset
            w_divid['100'].append(W_AB_100[idx])
            w_diff['100'].append(W_A_B_100[idx])
            w_divid['010'].append(W_AB_010[idx])
            w_diff['010'].append(W_A_B_010[idx])
            w_divid['001'].append(W_AB_001[idx])
            w_diff['001'].append(W_A_B_001[idx])
            w_divid['910'].append(W_AB_910[idx])
            w_diff['910'].append(W_A_B_910[idx])
            w_divid['820'].append(W_AB_820[idx])
            w_diff['820'].append(W_A_B_820[idx])
            w_divid['730'].append(W_AB_730[idx])
            w_diff['730'].append(W_A_B_730[idx])
            w_divid['640'].append(W_AB_640[idx])
            w_diff['640'].append(W_A_B_640[idx])
            w_divid['550'].append(W_AB_550[idx])
            w_diff['550'].append(W_A_B_550[idx])
            w_divid['721'].append(W_AB_721[idx])
            w_diff['721'].append(W_A_B_721[idx])
            w_divid['532'].append(W_AB_532[idx])
            w_diff['532'].append(W_A_B_532[idx])
            w_divid['111'].append(W_AB_111[idx])
            w_diff['111'].append(W_A_B_111[idx])
            w_divid['190'].append(W_AB_190[idx])
            w_diff['190'].append(W_A_B_190[idx])
            w_divid['280'].append(W_AB_280[idx])
            w_diff['280'].append(W_A_B_280[idx])
            w_divid['370'].append(W_AB_370[idx])
            w_diff['370'].append(W_A_B_370[idx])
            w_divid['460'].append(W_AB_460[idx])
            w_diff['460'].append(W_A_B_460[idx])
            w_divid['127'].append(W_AB_127[idx])
            w_diff['127'].append(W_A_B_127[idx])
            w_divid['235'].append(W_AB_235[idx])
            w_diff['235'].append(W_A_B_235[idx])
            
        elif len(index_array) == 0:
            # 当前秒无数据,使用上一秒的数据
            if i < 25200 - traded_time:
                index_min = np.where(time_second_basic <= i + traded_time)[0][-1]
                traded_min = ask_price_1[index:index_min]
                if bid_price_1[index] > np.min(traded_min):
                    traded.append(1)
                else:
                    traded.append(0)
            else:
                if bid_price_1[index] > ask_price_1[-1]:
                    traded.append(1)
                else:
                    traded.append(0)
            
            # 复制上一秒的特征值
            for j in range(30):
                rise_ratio_second[j].append(rise_ratio_second[j][-1])
            
            for key in w_divid.keys():
                w_divid[key].append(w_divid[key][-1])
                w_diff[key].append(w_diff[key][-1])
    
    # 返回所有数据
    return (traded, index_,
            *rise_ratio_second,
            w_divid['100'], w_diff['100'], w_divid['010'], w_diff['010'],
            w_divid['001'], w_diff['001'], w_divid['910'], w_diff['910'],
            w_divid['820'], w_diff['820'], w_divid['730'], w_diff['730'],
            w_divid['640'], w_diff['640'], w_divid['550'], w_diff['550'],
            w_divid['721'], w_diff['721'], w_divid['532'], w_diff['532'],
            w_divid['111'], w_diff['111'], w_divid['190'], w_diff['190'],
            w_divid['280'], w_diff['280'], w_divid['370'], w_diff['370'],
            w_divid['460'], w_diff['460'], w_divid['127'], w_diff['127'],
            w_divid['235'], w_diff['235'])


def Feature_DataFrame_UP(traded_time, time_second_basic, bid_price_1, ask_price_1,
                         rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
                         rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
                         rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
                         rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
                         rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
                         rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
                         rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
                         rise_ratio_ask_29, rise_ratio_ask_30,
                         W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
                         W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
                         W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
                         W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
                         W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
                         W_AB_127, W_A_B_127, W_AB_235, W_A_B_235):
    """
    构建上午时段(09:00-11:30)的特征DataFrame
    
    返回:
        pd.DataFrame: 包含64列特征的数据框
            - 第0列: 交易标签
            - 第1-30列: 30个涨跌比率特征
            - 第31-64列: 34个深度特征
    """
    # 上午时段: 09:00 ~ 11:30 (0秒 ~ 9000秒)
    time1 = 0
    time2 = 9000
    
    print(f'[特征提取] 上午时段特征数量: {len(W_AB_910)}')
    
    # 调用交易标签生成函数
    result = traded_label_one_second(
        time1, time2, time_second_basic, bid_price_1, ask_price_1, traded_time,
        rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
        rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
        rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
        rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
        rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
        rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
        rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
        rise_ratio_ask_29, rise_ratio_ask_30,
        W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
        W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
        W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
        W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
        W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
        W_AB_127, W_A_B_127, W_AB_235, W_A_B_235
    )
    
    # 解包返回结果
    traded = result[0]
    rise_ratios = result[2:32]  # 30个涨跌比率
    depth_features = result[32:]  # 34个深度特征
    
    # 构建数据数组
    data = np.array([traded, *rise_ratios, *depth_features]).T
    
    return pd.DataFrame(data)


def Feature_DataFrame_DOWN(traded_time, time_second_basic, bid_price_1, ask_price_1,
                           rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
                           rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
                           rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
                           rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
                           rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
                           rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
                           rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
                           rise_ratio_ask_29, rise_ratio_ask_30,
                           W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
                           W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
                           W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
                           W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
                           W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
                           W_AB_127, W_A_B_127, W_AB_235, W_A_B_235):
    """
    构建下午时段(13:00-16:00)的特征DataFrame
    
    返回:
        pd.DataFrame: 包含64列特征的数据框
    """
    # 下午时段: 13:00 ~ 16:00 (14400秒 ~ 25200秒)
    time1 = 14400
    time2 = 25200
    
    # 调用交易标签生成函数
    result = traded_label_one_second(
        time1, time2, time_second_basic, bid_price_1, ask_price_1, traded_time,
        rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
        rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
        rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
        rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
        rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
        rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
        rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
        rise_ratio_ask_29, rise_ratio_ask_30,
        W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
        W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
        W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
        W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
        W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
        W_AB_127, W_A_B_127, W_AB_235, W_A_B_235
    )
    
    # 解包返回结果
    traded = result[0]
    rise_ratios = result[2:32]
    depth_features = result[32:]
    
    # 构建数据数组
    data = np.array([traded, *rise_ratios, *depth_features]).T
    
    return pd.DataFrame(data)


def data(month, day, traded_time, data_path='./'):
    """
    主数据处理函数,计算所有特征并生成上下午数据框
    
    参数:
        month: 月份
        day: 日期
        traded_time: 交易预测时间窗口(秒),默认600秒
        data_path: 数据文件路径
    
    返回:
        data_2014_UP: 上午时段特征DataFrame
        data_2014_DOWN: 下午时段特征DataFrame
        len_: 数据长度
    """
    # 读取订单簿数据
    (timestamp, order_book_, bid_price_1, bid_price_2, bid_price_3,
     bid_quantity_1, bid_quantity_2, bid_quantity_3,
     ask_price_1, ask_price_2, ask_price_3, 
     ask_quantity_1, ask_quantity_2, ask_quantity_3) = order_book(month, day, data_path)
    
    # 时间转换
    time_second, time_second_basic = time_transform(timestamp)
    
    # 提取09:00之后的卖一价
    Ask1 = ask_price_1[np.where(time_second_basic <= 0.0)[0][-1]:]
    
    # 计算30种涨跌比率特征(时间窗口从6分钟到20.5分钟)
    print('[特征提取] 计算30种涨跌比率特征...')
    
    rise_ratio_ask_1 = rise_ask(Ask1, time_second_basic, 60.0 * 6)
    rise_ratio_ask_2 = rise_ask(Ask1, time_second_basic, 60.0 * 6 + 30)
    rise_ratio_ask_3 = rise_ask(Ask1, time_second_basic, 60.0 * 7)
    rise_ratio_ask_4 = rise_ask(Ask1, time_second_basic, 60.0 * 7 + 30)
    rise_ratio_ask_5 = rise_ask(Ask1, time_second_basic, 60.0 * 8)
    rise_ratio_ask_6 = rise_ask(Ask1, time_second_basic, 60.0 * 8 + 30)
    rise_ratio_ask_7 = rise_ask(Ask1, time_second_basic, 60.0 * 9)
    rise_ratio_ask_8 = rise_ask(Ask1, time_second_basic, 60.0 * 9 + 30)
    rise_ratio_ask_9 = rise_ask(Ask1, time_second_basic, 60.0 * 10)
    rise_ratio_ask_10 = rise_ask(Ask1, time_second_basic, 60.0 * 10 + 30)
    rise_ratio_ask_11 = rise_ask(Ask1, time_second_basic, 60.0 * 11)
    rise_ratio_ask_12 = rise_ask(Ask1, time_second_basic, 60.0 * 11 + 30)
    rise_ratio_ask_13 = rise_ask(Ask1, time_second_basic, 60.0 * 12)
    rise_ratio_ask_14 = rise_ask(Ask1, time_second_basic, 60.0 * 12 + 30)
    rise_ratio_ask_15 = rise_ask(Ask1, time_second_basic, 60.0 * 13)
    rise_ratio_ask_16 = rise_ask(Ask1, time_second_basic, 60.0 * 13 + 30)
    rise_ratio_ask_17 = rise_ask(Ask1, time_second_basic, 60.0 * 14)
    rise_ratio_ask_18 = rise_ask(Ask1, time_second_basic, 60.0 * 14 + 30)
    rise_ratio_ask_19 = rise_ask(Ask1, time_second_basic, 60.0 * 15)
    rise_ratio_ask_20 = rise_ask(Ask1, time_second_basic, 60.0 * 15 + 30)
    rise_ratio_ask_21 = rise_ask(Ask1, time_second_basic, 60.0 * 16)
    rise_ratio_ask_22 = rise_ask(Ask1, time_second_basic, 60.0 * 16 + 30)
    rise_ratio_ask_23 = rise_ask(Ask1, time_second_basic, 60.0 * 17)
    rise_ratio_ask_24 = rise_ask(Ask1, time_second_basic, 60.0 * 17 + 30)
    rise_ratio_ask_25 = rise_ask(Ask1, time_second_basic, 60.0 * 18)
    rise_ratio_ask_26 = rise_ask(Ask1, time_second_basic, 60.0 * 18 + 30)
    rise_ratio_ask_27 = rise_ask(Ask1, time_second_basic, 60.0 * 19)
    rise_ratio_ask_28 = rise_ask(Ask1, time_second_basic, 60.0 * 19 + 30)
    rise_ratio_ask_29 = rise_ask(Ask1, time_second_basic, 60.0 * 20)
    rise_ratio_ask_30 = rise_ask(Ask1, time_second_basic, 60.0 * 20 + 30)
    
    # 计算17种权重组合的深度特征
    print('[特征提取] 计算17种深度特征...')
    
    W_AB_100, W_A_B_100 = weight_percentage(100.0, 0.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_010, W_A_B_010 = weight_percentage(0.0, 100.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_001, W_A_B_001 = weight_percentage(0.0, 0.0, 100.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_910, W_A_B_910 = weight_percentage(90.0, 10.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_820, W_A_B_820 = weight_percentage(80.0, 20.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_730, W_A_B_730 = weight_percentage(70.0, 30.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_640, W_A_B_640 = weight_percentage(60.0, 40.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_550, W_A_B_550 = weight_percentage(50.0, 50.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_721, W_A_B_721 = weight_percentage(70.0, 20.0, 10.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_532, W_A_B_532 = weight_percentage(50.0, 30.0, 20.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_111, W_A_B_111 = weight_percentage(1.0, 1.0, 1.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_190, W_A_B_190 = weight_percentage(10.0, 90.0, 1.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_280, W_A_B_280 = weight_percentage(20.0, 80.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_370, W_A_B_370 = weight_percentage(30.0, 70.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_460, W_A_B_460 = weight_percentage(40.0, 60.0, 0.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_127, W_A_B_127 = weight_percentage(10.0, 20.0, 70.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    W_AB_235, W_A_B_235 = weight_percentage(20.0, 30.0, 50.0, ask_quantity_1, ask_quantity_2, ask_quantity_3,
                                            bid_quantity_1, bid_quantity_2, bid_quantity_3)
    
    # 构建上午和下午的特征DataFrame
    print('[特征提取] 构建特征数据框...')
    
    data_2014_UP = Feature_DataFrame_UP(
        traded_time, time_second_basic, bid_price_1, ask_price_1,
        rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
        rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
        rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
        rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
        rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
        rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
        rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
        rise_ratio_ask_29, rise_ratio_ask_30,
        W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
        W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
        W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
        W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
        W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
        W_AB_127, W_A_B_127, W_AB_235, W_A_B_235
    )
    
    data_2014_DOWN = Feature_DataFrame_DOWN(
        traded_time, time_second_basic, bid_price_1, ask_price_1,
        rise_ratio_ask_1, rise_ratio_ask_2, rise_ratio_ask_3, rise_ratio_ask_4,
        rise_ratio_ask_5, rise_ratio_ask_6, rise_ratio_ask_7, rise_ratio_ask_8,
        rise_ratio_ask_9, rise_ratio_ask_10, rise_ratio_ask_11, rise_ratio_ask_12,
        rise_ratio_ask_13, rise_ratio_ask_14, rise_ratio_ask_15, rise_ratio_ask_16,
        rise_ratio_ask_17, rise_ratio_ask_18, rise_ratio_ask_19, rise_ratio_ask_20,
        rise_ratio_ask_21, rise_ratio_ask_22, rise_ratio_ask_23, rise_ratio_ask_24,
        rise_ratio_ask_25, rise_ratio_ask_26, rise_ratio_ask_27, rise_ratio_ask_28,
        rise_ratio_ask_29, rise_ratio_ask_30,
        W_AB_100, W_A_B_100, W_AB_010, W_A_B_010, W_AB_001, W_A_B_001,
        W_AB_910, W_A_B_910, W_AB_820, W_A_B_820, W_AB_730, W_A_B_730,
        W_AB_640, W_A_B_640, W_AB_550, W_A_B_550, W_AB_721, W_A_B_721,
        W_AB_532, W_A_B_532, W_AB_111, W_A_B_111, W_AB_190, W_A_B_190,
        W_AB_280, W_A_B_280, W_AB_370, W_A_B_370, W_AB_460, W_A_B_460,
        W_AB_127, W_A_B_127, W_AB_235, W_A_B_235
    )
    
    return data_2014_UP, data_2014_DOWN, len(W_AB_111)


def train_test_to_csv(month, day, traded_time, data_path='./', output_path='./'):
    """
    生成训练测试数据并保存为CSV文件
    
    参数:
        month: 月份
        day: 日期
        traded_time: 交易预测时间窗口(秒)
        data_path: 输入数据路径
        output_path: 输出数据路径
    """
    print(f'[数据处理] 开始处理 2014-{month}-{day} 数据...')
    
    data_UP, data_DOWN, len_ = data(month, day, traded_time, data_path)
    
    # 构建输出文件路径
    path_up = os.path.join(output_path, f'order_book_3_2014_{month}_{day}_UP.csv')
    path_down = os.path.join(output_path, f'order_book_3_2014_{month}_{day}_DOWN.csv')
    
    # 保存为CSV
    data_UP.to_csv(path_up, index=False)
    data_DOWN.to_csv(path_down, index=False)
    
    print(f'[数据处理] 上午数据已保存: {path_up}')
    print(f'[数据处理] 下午数据已保存: {path_down}')
    print(f'[数据处理] 数据长度: {len_}')


# 主程序示例
if __name__ == '__main__':
    # 配置参数
    month = 1
    day_list = [2]
    traded_time = 600  # 10分钟预测窗口
    
    # 使用当前目录的数据文件
    data_path = './'
    output_path = './'
    
    print('[Train_Test_Builder_v3.py] 开始执行')
    print(f'数据路径: {data_path}')
    print(f'输出路径: {output_path}')
    print(f'交易时间窗口: {traded_time}秒')
    print('')
    
    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)
    
    # 处理每一天的数据
    for day in day_list:
        print(f'[主程序] 处理交易日: {month}月{day}日')
        try:
            train_test_to_csv(month, day, traded_time, data_path, output_path)
            print(f'[主程序] ✅ {month}-{day} 处理成功')
            print(f'  输出文件: order_book_3_2014_{month}_{day}_UP.csv')
            print(f'  输出文件: order_book_3_2014_{month}_{day}_DOWN.csv')
        except FileNotFoundError as e:
            print(f'[主程序] ⚠️  文件未找到: {e}')
            print('[主程序] 请确保 order_book_3_2014_1_2.csv 存在于当前目录')
        except Exception as e:
            print(f'[主程序] ❌ 处理出错: {e}')
            import traceback
            traceback.print_exc()
    
    print('\n[主程序] 所有数据处理完成!')
