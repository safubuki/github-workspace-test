#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
買い物リスト管理と電卓機能を持つPythonアプリケーション
Shopping List Manager with Calculator Functionality

このアプリケーションは買い物時に便利な機能を提供します：
- 四則演算（電卓機能）
- 買い物リストの作成・編集・管理
- JSONファイルでのリスト永続化
"""

import os
import sys

from calculator import Calculator
from shopping_list import ShoppingList


class ShoppingCalculatorApp:
    """メインアプリケーションクラス
    
    電卓機能と買い物リスト管理を統合したアプリケーションを提供します。
    Main application class that integrates calculator and shopping list functionality.
    """
    
    def __init__(self):
        """ShoppingCalculatorAppクラスの初期化
        
        電卓とショッピングリストのインスタンスを作成し、アプリケーション状態を初期化します。
        """
        self.calculator = Calculator()
        self.shopping_list = ShoppingList()
        self.running = True
    
    def display_menu(self):
        """メインメニューを表示
        
        アプリケーションの主要機能を選択するためのメニューを表示します。
        """
        print("\n" + "="*50)
        print("    買い物リスト & 電卓アプリケーション")
        print("="*50)
        print("1. 電卓機能")
        print("2. 買い物リスト管理")
        print("3. リスト保存")
        print("4. リスト読み込み")
        print("5. アプリケーション終了")
        print("-"*50)
    
    def calculator_menu(self):
        """電卓メニューを表示・実行
        
        電卓の各種機能（簡単計算、式計算、履歴表示など）のサブメニューを提供します。
        """
        while True:
            print("\n" + "-"*30)
            print("    電卓機能")
            print("-"*30)
            print("1. 簡単計算 (数値入力)")
            print("2. 式計算 (式を入力)")
            print("3. 計算履歴表示")
            print("4. 履歴クリア")
            print("5. メインメニューに戻る")
            
            try:
                choice = input("選択してください (1-5): ").strip()
                
                if choice == "1":
                    self.simple_calculation()
                elif choice == "2":
                    self.expression_calculation()
                elif choice == "3":
                    self.show_calculation_history()
                elif choice == "4":
                    self.clear_calculation_history()
                elif choice == "5":
                    break
                else:
                    print("無効な選択です。1-5の数字を入力してください")
            except Exception as e:
                print(f"エラーが発生しました: {e}")
    
    def simple_calculation(self):
        """簡単計算（2つの数値と演算子）を実行
        
        ユーザーから2つの数値と演算子を入力として受け取り、計算を実行します。
        """
        try:
            num1 = float(input("最初の数値を入力してください: "))
            operator = input("演算子を入力してください (+, -, ×, ÷): ").strip()
            num2 = float(input("次の数値を入力してください: "))
            
            if operator == "+":
                result = self.calculator.add(num1, num2)
            elif operator == "-":
                result = self.calculator.subtract(num1, num2)
            elif operator in ["×", "*"]:
                result = self.calculator.multiply(num1, num2)
            elif operator in ["÷", "/"]:
                result = self.calculator.divide(num1, num2)
            else:
                print("無効な演算子です")
                return
            
            print(f"結果: {result}")
        except ValueError as e:
            print(f"計算エラー: {e}")
        except Exception as e:
            print(f"入力エラー: {e}")
    
    def expression_calculation(self):
        """式計算（文字列で数式を入力）を実行
        
        ユーザーから数式を文字列として受け取り、評価・計算を実行します。
        """
        try:
            expression = input("計算式を入力してください (例: 100 + 200 * 1.08): ").strip()
            result = self.calculator.calculate_expression(expression)
            print(f"結果: {result}")
        except ValueError as e:
            print(f"計算エラー: {e}")
        except Exception as e:
            print(f"入力エラー: {e}")
    
    def show_calculation_history(self):
        """計算履歴を表示
        
        過去に実行された計算の履歴を一覧表示します。
        """
        history = self.calculator.get_history()
        if history:
            print("\n=== 計算履歴 ===")
            for i, calc in enumerate(history, 1):
                print(f"{i}. {calc}")
        else:
            print("計算履歴がありません")
    
    def clear_calculation_history(self):
        """計算履歴をクリア
        
        保存されている計算履歴を全て削除します。
        """
        self.calculator.clear_history()
        print("計算履歴をクリアしました")
    
    def shopping_list_menu(self):
        """買い物リストメニューを表示・実行
        
        買い物リストの各種操作（追加、削除、完了、表示など）のサブメニューを提供します。
        """
        while True:
            print("\n" + "-"*30)
            print("    買い物リスト管理")
            print("-"*30)
            print("1. アイテム追加")
            print("2. アイテム削除")
            print("3. アイテム完了")
            print("4. リスト表示")
            print("5. 合計金額表示")
            print("6. メインメニューに戻る")
            
            try:
                choice = input("選択してください (1-6): ").strip()
                
                if choice == "1":
                    self.add_shopping_item()
                elif choice == "2":
                    self.remove_shopping_item()
                elif choice == "3":
                    self.complete_shopping_item()
                elif choice == "4":
                    self.display_shopping_list()
                elif choice == "5":
                    self.display_total()
                elif choice == "6":
                    break
                else:
                    print("無効な選択です。1-6の数字を入力してください")
            except Exception as e:
                print(f"エラーが発生しました: {e}")
    
    def add_shopping_item(self):
        """買い物アイテムを追加
        
        ユーザーからアイテム名、数量、価格を入力として受け取り、買い物リストに追加します。
        """
        try:
            name = input("アイテム名を入力してください: ").strip()
            if not name:
                print("アイテム名を入力してください")
                return
            
            quantity_str = input("数量を入力してください (デフォルト: 1): ").strip()
            quantity = int(quantity_str) if quantity_str else 1
            
            price_str = input("価格を入力してください (オプション): ").strip()
            price = float(price_str) if price_str else None
            
            message = self.shopping_list.add_item(name, quantity, price)
            print(message)
        except ValueError:
            print("数値の入力が正しくありません")
        except Exception as e:
            print(f"追加エラー: {e}")
    
    def remove_shopping_item(self):
        """買い物アイテムを削除
        
        ユーザーが指定したインデックスのアイテムを買い物リストから削除します。
        """
        try:
            items = self.shopping_list.get_items()
            if not items:
                print("リストにアイテムがありません")
                return
            
            self.display_shopping_list()
            index = int(input("削除するアイテム番号を入力してください: ")) - 1
            message = self.shopping_list.remove_item(index)
            print(message)
        except (ValueError, IndexError) as e:
            print(f"削除エラー: {e}")
        except Exception as e:
            print(f"削除エラー: {e}")
    
    def complete_shopping_item(self):
        """買い物アイテムを完了
        
        ユーザーが指定したアイテムを完了済みリストに移動します。
        """
        try:
            items = self.shopping_list.get_items()
            if not items:
                print("リストにアイテムがありません")
                return
            
            self.display_shopping_list()
            index = int(input("完了するアイテム番号を入力してください: ")) - 1
            message = self.shopping_list.complete_item(index)
            print(message)
        except (ValueError, IndexError) as e:
            print(f"完了エラー: {e}")
        except Exception as e:
            print(f"完了エラー: {e}")
    
    def display_shopping_list(self):
        """買い物リストを表示
        
        未完了および完了済みのアイテムを整理して表示します。
        """
        items = self.shopping_list.get_items()
        completed_items = self.shopping_list.get_completed_items()
        
        print("\n=== 買い物リスト ===")
        
        if items:
            print("【未完了アイテム】")
            for i, item in enumerate(items, 1):
                price_str = f" - ¥{item['price']}" if item['price'] else ""
                print(f"{i}. {item['name']} (数量: {item['quantity']}){price_str}")
        else:
            print("【未完了アイテム】\n(なし)")
        
        if completed_items:
            print("\n【完了済みアイテム】")
            for item in completed_items:
                price_str = f" - ¥{item['price']}" if item['price'] else ""
                print(f"✓ {item['name']} (数量: {item['quantity']}){price_str}")
    
    def display_total(self):
        """合計金額を計算・表示
        
        価格が設定された未完了アイテムの合計金額を計算し表示します。
        """
        total = self.shopping_list.calculate_total()
        if total > 0:
            print(f"\n価格設定済みアイテムの合計金額: ¥{total}")
        else:
            print("\n価格が設定されたアイテムがありません")
    
    def save_list(self):
        """リストをファイルに保存
        
        ユーザーが指定したファイル名で買い物リストをJSONファイルに保存します。
        """
        try:
            filename = input("保存ファイル名を入力 (.json): ").strip()
            if not filename.endswith('.json'):
                filename += '.json'
            
            message = self.shopping_list.save_to_file(filename)
            print(message)
        except Exception as e:
            print(f"保存エラー: {e}")
    
    def load_list(self):
        """ファイルからリストを読み込み
        
        ユーザーが指定したJSONファイルから買い物リストを読み込みます。
        """
        try:
            filename = input("読み込みファイル名を入力: ").strip()
            message = self.shopping_list.load_from_file(filename)
            print(message)
        except Exception as e:
            print(f"読み込みエラー: {e}")
    
    def run(self):
        """アプリケーションのメインループ
        
        アプリケーションの主要な実行ループを管理し、ユーザーの入力に基づいて
        適切な機能を呼び出します。
        """
        print("買い物リスト & 電卓アプリケーションを開始します")
        
        # 起動時にショッピングリストの状況を表示
        items = self.shopping_list.get_items()
        completed_items = self.shopping_list.get_completed_items()
        if items or completed_items:
            print(f"保存されたリストを読み込みました：未完了 {len(items)} 件、完了済み {len(completed_items)} 件")
        
        while self.running:
            try:
                self.display_menu()
                choice = input("選択してください (1-5): ").strip()
                
                if choice == "1":
                    self.calculator_menu()
                elif choice == "2":
                    self.shopping_list_menu()
                elif choice == "3":
                    self.save_list()
                elif choice == "4":
                    self.load_list()
                elif choice == "5":
                    print("アプリケーションを終了します")
                    self.running = False
                else:
                    print("無効な選択です。1-5の数字を入力してください")
            
            except KeyboardInterrupt:
                print("\n\nアプリケーションを終了します")
                self.running = False
            except Exception as e:
                print(f"予期しないエラーが発生しました: {e}")


def main():
    """メイン関数
    
    アプリケーションのエントリーポイント。ShoppingCalculatorAppのインスタンスを
    作成し、メインループを開始します。
    
    Returns:
        None
    """
    app = ShoppingCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()