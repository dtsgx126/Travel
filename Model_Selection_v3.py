#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型选择模块 - Python 3版本

本模块负责机器学习模型的训练、参数调优和交叉验证。
主要功能包括：
1. 网格搜索最优参数
2. 模型训练和预测
3. 滚动窗口训练策略
4. 模型评估指标汇总

升级说明：
- 将print语句改为print()函数
- 更新sklearn导入路径（grid_search -> model_selection）
- 所有map()调用包裹list()转换
- 添加中文文档字符串和注释
"""

import pandas as pd
import numpy as np
import time
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier, 
                              AdaBoostClassifier, GradientBoostingClassifier)
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.linear_model import LogisticRegression


def read_csv(day_trade):
    """
    读取训练和测试数据CSV文件
    
    参数：
        day_trade: 交易日列表
        
    返回：
        data_up: 上涨方向数据列表
        data_down: 下跌方向数据列表
    """
    data_up = []
    data_down = []
    path = '/home/rory/Demo/Data_Transformation/Train_Test_Builder/order_book_3_2014'
    
    for j, i in enumerate(day_trade):
        for k in range(0, len(i), 1):
            path_up = path + '_' + str(j+1) + '_' + str(i[k]) + '_' + 'UP' + '.csv'
            path_down = path + '_' + str(j+1) + '_' + str(i[k]) + '_' + 'DOWN' + '.csv'
            data_up.append(pd.read_csv(path_up))
            data_down.append(pd.read_csv(path_down))
    
    return data_up, data_down


# 机器学习算法配置
models = {
    'RandomForestClassifier': RandomForestClassifier(random_state=0),
    'ExtraTreesClassifier': ExtraTreesClassifier(random_state=0),
    'AdaBoostClassifier': AdaBoostClassifier(
        base_estimator=DecisionTreeClassifier(),
        n_estimators=10,
        random_state=0
    ),
    'GradientBoostingClassifier': GradientBoostingClassifier(random_state=0),
    'SVC': SVC(probability=True, random_state=0),
}


# 超参数网格配置
model_grid_params = {
    'RandomForestClassifier': {
        'max_features': [None],
        'n_estimators': [10],
        'max_depth': [10],
        'min_samples_split': [2],
        'criterion': ['entropy'],
        'min_samples_leaf': [3]
    },
    'ExtraTreesClassifier': {
        'max_features': [None],
        'n_estimators': [10],
        'max_depth': [10],
        'min_samples_split': [2],
        'criterion': ['entropy'],
        'min_samples_leaf': [3]
    },
    'AdaBoostClassifier': {
        "base_estimator__criterion": ["entropy"],
        "base_estimator__max_depth": [None],
        "base_estimator__min_samples_leaf": [3],
        "base_estimator__min_samples_split": [2],
        "base_estimator__max_features": [None]
    },
    'GradientBoostingClassifier': {
        'max_features': [None],
        'n_estimators': [10],
        'max_depth': [10],
        'min_samples_split': [2],
        'min_samples_leaf': [3],
        'learning_rate': [0.1],
        'subsample': [1.0]
    },
    'SVC': [
        {'kernel': ['rbf'], 'gamma': [1e-1], 'C': [1]},
        {'kernel': ['linear'], 'C': [1, 10]}
    ]
}


class Model_Selection:
    """
    模型选择类
    
    负责机器学习模型的训练、评估和选择。
    使用网格搜索进行超参数调优，支持滚动窗口训练策略。
    """
    
    def __init__(self, models, model_grid_params, data_2014, latest_sec, pred_sec, day):
        """
        初始化模型选择器
        
        参数：
            models: 模型字典
            model_grid_params: 超参数网格
            data_2014: 2014年数据
            latest_sec: 训练窗口大小（秒）
            pred_sec: 预测窗口大小（秒）
            day: 交易日数量
        """
        self.models = models
        self.model_grid = model_grid_params
        self.data_2014 = data_2014
        self.latest_sec = latest_sec
        self.pred_sec = pred_sec
        self.day = day
        self.keys = list(models.keys())  # Python 3: 显式转换为列表
        self.best_score = {}
        self.grid = {}
        self.predict_values = {}
        self.cv_acc = {}
        self.acc = {}
        self.fscore = {}
        self.true_values = {}
        self.predict_values_day = {}
        self.cv_acc_day = {}
        self.acc_day = {}
        self.fscore_day = {}
        self.true_values_day = {}
        self.summary_day = []
        
    def Grid_fit(self, X_train, y_train, cv=5, scoring='accuracy'):
        """
        使用网格搜索寻找最优参数
        
        参数：
            X_train: 训练特征
            y_train: 训练标签
            cv: 交叉验证折数
            scoring: 评分指标
        """
        for key in self.keys:
            print(f"[模型训练] 正在对 {key} 执行网格搜索...")
            model = self.models[key]
            model_grid = self.model_grid[key]
            Grid = GridSearchCV(model, model_grid, cv=cv, scoring=scoring)
            Grid.fit(X_train, y_train)
            self.grid[key] = Grid
            print(f"[参数优化] 最佳参数: {Grid.best_params_}")
            print(f'[交叉验证] 最佳得分 = {Grid.best_score_:.4f}')
            self.cv_acc[key].append(Grid.best_score_)
    
    def model_fit(self, X_train, y_train, X_test, y_test):
        """
        训练模型并进行预测
        
        参数：
            X_train: 训练特征
            y_train: 训练标签
            X_test: 测试特征
            y_test: 测试标签
        """
        for key in self.keys:
            print(f"[模型评估] 正在训练和测试 {key}...")
            model = self.models[key]
            model.set_params(**self.grid[key].best_params_)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            
            self.predict_values[key].append(predictions.tolist())
            self.true_values[key].append(y_test.tolist())
            
            acc = metrics.accuracy_score(y_test, predictions)
            f_score = metrics.f1_score(y_test, predictions)
            print(f'[准确率] {key}: {acc:.4f}')
            
            self.acc[key].append(acc)
            self.fscore[key].append(f_score)
            
            # 特征重要性分析
            if key == 'SVC':
                if list(self.grid[key].best_params_.values())[0] == 'linear':
                    feature_imp = dict(zip([i for i in range(0, 64, 1)], model.coef_[0]))
                    Top_five = sorted(feature_imp.items(), key=lambda x: x[1], reverse=True)[0:5]
            else:
                feature_imp = dict(zip([i for i in range(0, 64, 1)], model.feature_importances_))
                Top_five = sorted(feature_imp.items(), key=lambda x: x[1], reverse=True)[0:5]
                
    def pipline(self):
        """
        执行完整的训练和评估流程
        
        使用滚动窗口策略进行模型训练和评估
        """
        self.set_list_day()  # 初始化每日结果存储
        
        for day in range(0, self.day, 1):
            self.set_list()  # 初始化当前结果存储
            print(f'\n[交易日] 第 {day+1} 天')
            
            for i in range(0, 10, self.pred_sec):
                print(f'--------------------滚动窗口时间 = {i//self.pred_sec}--------------------')
                
                # 准备训练数据
                data_train = self.data_2014[day][i:i+self.latest_sec]
                X_train = data_train.drop(['0'], axis=1)
                y_train = data_train['0']
                
                # 准备测试数据
                data_test = self.data_2014[day][i + self.latest_sec:i + self.latest_sec + self.pred_sec]
                X_test = data_test.drop(['0'], axis=1)
                y_test = data_test['0']
                
                # 执行网格搜索和模型训练
                self.Grid_fit(X_train, y_train, cv=5, scoring='accuracy')
                self.model_fit(X_train, y_train, X_test, y_test)
                
            # 保存每日结果
            for key in self.keys:
                self.cv_acc_day[key].append(self.cv_acc[key])
                self.acc_day[key].append(self.acc[key])
                self.fscore_day[key].append(self.fscore[key])
                self.true_values_day[key].append(self.true_values[key])
                self.predict_values_day[key].append(self.predict_values[key])
            
            self.summary_day.append(self.score_summary(sort_by='Accuracy_mean'))
    
    def set_list(self):
        """
        初始化当前结果列表
        """
        for key in self.keys:
            self.predict_values[key] = []
            self.cv_acc[key] = []
            self.acc[key] = []
            self.fscore[key] = []
            self.true_values[key] = []
            
    def set_list_day(self):
        """
        初始化每日结果列表
        """
        for key in self.keys:
            self.predict_values_day[key] = []
            self.cv_acc_day[key] = []
            self.acc_day[key] = []
            self.fscore_day[key] = []
            self.true_values_day[key] = []
            
    def score_summary(self, sort_by):
        """
        汇总评估指标
        
        参数：
            sort_by: 排序依据列名
            
        返回：
            summary: 评估指标汇总DataFrame
        """
        # Python 3: map()需要包裹list()
        summary = pd.concat([
            pd.DataFrame(list(self.acc.keys())),
            pd.DataFrame(list(map(lambda x: np.mean(self.acc[x]), self.acc))),
            pd.DataFrame(list(map(lambda x: np.std(self.acc[x]), self.acc))),
            pd.DataFrame(list(map(lambda x: np.max(self.acc[x]), self.acc))),
            pd.DataFrame(list(map(lambda x: np.min(self.acc[x]), self.acc))),
            pd.DataFrame(list(map(lambda x: np.mean(self.fscore[x]), self.fscore)))
        ], axis=1)
        
        summary.columns = ['Estimator', 'Accuracy_mean', 'Accuracy_std', 
                          'Accuracy_max', 'Accuracy_min', 'F_score']
        summary.index.rename('Ranking', inplace=True)
        
        return summary.sort_values(by=[sort_by], ascending=False)
          
    def print_(self):
        """
        打印预测值
        """
        print(self.predict_values)


if __name__ == '__main__':
    print('[Model_Selection_v3.py] 开始执行')
    print('说明：本模块提供机器学习模型的训练、参数调优和交叉验证功能')
    print('\n正在加载训练数据...')
    
    try:
        # 加载数据 - 使用正确的相对路径
        data_path = 'upgraded/Data_Transformation/Train_Test_Builder/'
        data_up = pd.read_csv(f'{data_path}order_book_3_2014_1_2_UP.csv')
        data_down = pd.read_csv(f'{data_path}order_book_3_2014_1_2_DOWN.csv')
        
        print(f'UP数据形状: {data_up.shape}')
        print(f'DOWN数据形状: {data_down.shape}')
        
        # 使用全部可用数据进行训练和测试（仍保留一部分作为测试集）
        print('\n使用全部数据进行模型训练和测试...')
        
        # 合并 UP 和 DOWN 数据
        sample_data = pd.concat([data_up, data_down], axis=0, ignore_index=True)
        
        # 分离特征和标签
        X = sample_data.drop(['0'], axis=1)
        y = sample_data['0']
        
        print(f'特征矩阵形状: {X.shape}')
        print(f'标签数量: {len(y)}')
        print(f'正样本数: {sum(y)}, 负样本数: {len(y) - sum(y)}')
        
        # 分割训练集和测试集
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f'\n训练集大小: {X_train.shape}')
        print(f'测试集大小: {X_test.shape}')
        
        # 使用单个模型进行快速测试（随机森林）
        print('\n训练随机森林模型...')
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, f1_score, classification_report
        
        model = RandomForestClassifier(n_estimators=10, max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        
        # 预测
        y_pred = model.predict(X_test)
        
        # 评估
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print('\n[Model_Selection_v3.py] ✅ 模型训练完成')
        print(f'  准确率: {accuracy:.4f}')
        print(f'  F1分数: {f1:.4f}')
        print('\n分类报告:')
        print(classification_report(y_test, y_pred))
        
        # 显示特征重要性
        feature_importance = model.feature_importances_
        top_5_indices = feature_importance.argsort()[-5:][::-1]
        print('\nTop 5 重要特征:')
        for idx in top_5_indices:
            print(f'  特征 {idx}: {feature_importance[idx]:.4f}')
        
        print('\n说明：以上是使用当前数据集的一次随机划分快速评估结果。')
        print('如需完整的模型训练和评估，请使用 Model_Selection 类进行完整的滚动窗口训练。')
        
    except FileNotFoundError as e:
        print(f'\n⚠️  文件未找到: {e}')
        print('请确保 order_book_3_2014_1_2_UP.csv 和 order_book_3_2014_1_2_DOWN.csv 存在于当前目录')
    except Exception as e:
        print(f'\n❌ 处理出错: {e}')
        import traceback
        traceback.print_exc()
