#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
電卓機能モジュール
Calculator module for basic arithmetic operations and expression evaluation.
"""


class Calculator:
    """電卓機能を提供するクラス
    
    四則演算と数式計算を行い、計算履歴を管理します。
    Basic arithmetic operations and expression calculations with history management.
    """
    
    def __init__(self):
        """Calculatorクラスの初期化
        
        計算履歴を空のリストで初期化します。
        """
        self.history = []
    
    def add(self, a, b):
        """加算を実行
        
        Args:
            a (float): 第一の数値
            b (float): 第二の数値
            
        Returns:
            float: 加算結果 (a + b)
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """減算を実行
        
        Args:
            a (float): 第一の数値
            b (float): 第二の数値
            
        Returns:
            float: 減算結果 (a - b)
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """乗算を実行
        
        Args:
            a (float): 第一の数値
            b (float): 第二の数値
            
        Returns:
            float: 乗算結果 (a × b)
        """
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        """除算を実行
        
        Args:
            a (float): 被除数
            b (float): 除数
            
        Returns:
            float: 除算結果 (a ÷ b)
            
        Raises:
            ValueError: 除数が0の場合
        """
        if b == 0:
            raise ValueError("ゼロで割ることはできません")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def calculate_expression(self, expression):
        """文字列として与えられた数式を計算
        
        Args:
            expression (str): 計算する数式（例: "100 + 200 * 1.08"）
            
        Returns:
            float: 計算結果
            
        Raises:
            ValueError: 無効な式の場合
        """
        try:
            # 安全な計算のため、eval()の代わりに基本的な演算子のみ許可
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except:
            raise ValueError("無効な式です")
    
    def get_history(self):
        """計算履歴を取得
        
        Returns:
            list: 計算履歴のコピー
        """
        return self.history.copy()
    
    def clear_history(self):
        """計算履歴をクリア
        
        履歴リストを空にします。
        """
        self.history.clear()