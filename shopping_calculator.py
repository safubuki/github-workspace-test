#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
買い物リスト管理と電卓機能を持つPythonアプリケーション
Shopping List Manager with Calculator Functionality

このアプリケーションは買い物時に便利な機能を提供します：
- 四則演算（電卓機能）
- 買い物リストの作成・編集・管理
- リストの保存・読み込み機能
"""

import os
import sys
from datetime import datetime


class Calculator:
    """電卓機能を提供するクラス"""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """加算"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """減算"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """乗算"""
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        """除算"""
        if b == 0:
            raise ValueError("ゼロで割ることはできません")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def calculate_expression(self, expression):
        """文字列として与えられた式を計算"""
        try:
            # 安全な計算のため、eval()の代わりに基本的な演算子のみ許可
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except:
            raise ValueError("無効な式です")
    
    def get_history(self):
        """計算履歴を取得"""
        return self.history.copy()
    
    def clear_history(self):
        """計算履歴をクリア"""
        self.history.clear()


class ShoppingList:
    """買い物リスト管理機能を提供するクラス"""
    
    def __init__(self):
        self.items = []
        self.completed_items = []
    
    def add_item(self, item, quantity=1, price=None):
        """アイテムをリストに追加"""
        item_data = {
            'name': item,
            'quantity': quantity,
            'price': price,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.items.append(item_data)
        return f"'{item}'をリストに追加しました"
    
    def remove_item(self, index):
        """指定されたインデックスのアイテムを削除"""
        if 0 <= index < len(self.items):
            removed_item = self.items.pop(index)
            return f"'{removed_item['name']}'をリストから削除しました"
        else:
            raise IndexError("無効なアイテム番号です")
    
    def complete_item(self, index):
        """アイテムを完了済みに移動"""
        if 0 <= index < len(self.items):
            completed_item = self.items.pop(index)
            completed_item['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.completed_items.append(completed_item)
            return f"'{completed_item['name']}'を完了しました"
        else:
            raise IndexError("無効なアイテム番号です")
    
    def get_items(self):
        """現在のアイテムリストを取得"""
        return self.items.copy()
    
    def get_completed_items(self):
        """完了済みアイテムを取得"""
        return self.completed_items.copy()
    
    def calculate_total(self):
        """価格が設定されているアイテムの合計金額を計算"""
        total = 0
        for item in self.items:
            if item['price']:
                total += item['price'] * item['quantity']
        return total
    
    def save_to_file(self, filename):
        """リストをテキストファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== 買い物リスト ===\n")
                f.write(f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("【未完了アイテム】\n")
                for i, item in enumerate(self.items):
                    price_str = f" - ¥{item['price']}" if item['price'] else ""
                    f.write(f"{i+1}. {item['name']} (数量: {item['quantity']}){price_str}\n")
                
                if self.completed_items:
                    f.write("\n【完了済みアイテム】\n")
                    for item in self.completed_items:
                        price_str = f" - ¥{item['price']}" if item['price'] else ""
                        f.write(f"✓ {item['name']} (数量: {item['quantity']}){price_str}\n")
                
                total = self.calculate_total()
                if total > 0:
                    f.write(f"\n合計金額: ¥{total}\n")
            
            return f"リストを '{filename}' に保存しました"
        except Exception as e:
            raise IOError(f"ファイル保存エラー: {e}")
    
    def load_from_file(self, filename):
        """テキストファイルからリストを読み込み"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.items.clear()
            self.completed_items.clear()
            
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith("【未完了アイテム】"):
                    current_section = "pending"
                elif line.startswith("【完了済みアイテム】"):
                    current_section = "completed"
                elif line and current_section == "pending" and line[0].isdigit():
                    # Parse item line: "1. item_name (数量: 2) - ¥100"
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        item_text = parts[1]
                        self.add_item(item_text.split(" (")[0])
                elif line and current_section == "completed" and line.startswith("✓"):
                    # Parse completed item
                    item_text = line[2:].strip()
                    item_data = {
                        'name': item_text.split(" (")[0],
                        'quantity': 1,
                        'price': None,
                        'completed_date': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    self.completed_items.append(item_data)
            
            return f"リストを '{filename}' から読み込みました"
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイル '{filename}' が見つかりません")
        except Exception as e:
            raise IOError(f"ファイル読み込みエラー: {e}")


class ShoppingCalculatorApp:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        self.calculator = Calculator()
        self.shopping_list = ShoppingList()
        self.running = True
    
    def display_menu(self):
        """メインメニューを表示"""
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
        """電卓メニューを表示・実行"""
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
                choice = input("\n選択してください (1-5): ").strip()
                
                if choice == "1":
                    self.simple_calculation()
                elif choice == "2":
                    self.expression_calculation()
                elif choice == "3":
                    self.show_calculation_history()
                elif choice == "4":
                    self.calculator.clear_history()
                    print("計算履歴をクリアしました")
                elif choice == "5":
                    break
                else:
                    print("無効な選択です")
            except KeyboardInterrupt:
                print("\n操作がキャンセルされました")
                break
    
    def simple_calculation(self):
        """簡単な計算を実行"""
        try:
            print("\n四則演算を行います")
            a = float(input("最初の数値を入力: "))
            operation = input("演算子を入力 (+, -, ×, ÷): ").strip()
            b = float(input("次の数値を入力: "))
            
            if operation == "+":
                result = self.calculator.add(a, b)
            elif operation == "-":
                result = self.calculator.subtract(a, b)
            elif operation == "×" or operation == "*":
                result = self.calculator.multiply(a, b)
            elif operation == "÷" or operation == "/":
                result = self.calculator.divide(a, b)
            else:
                print("無効な演算子です")
                return
            
            print(f"結果: {result}")
        except ValueError as e:
            print(f"エラー: {e}")
        except Exception as e:
            print(f"計算エラー: {e}")
    
    def expression_calculation(self):
        """式を入力して計算"""
        try:
            expression = input("計算式を入力 (例: 100 + 200 * 1.08): ").strip()
            result = self.calculator.calculate_expression(expression)
            print(f"結果: {result}")
        except ValueError as e:
            print(f"エラー: {e}")
        except Exception as e:
            print(f"計算エラー: {e}")
    
    def show_calculation_history(self):
        """計算履歴を表示"""
        history = self.calculator.get_history()
        if history:
            print("\n=== 計算履歴 ===")
            for i, calc in enumerate(history, 1):
                print(f"{i}. {calc}")
        else:
            print("計算履歴はありません")
    
    def shopping_list_menu(self):
        """買い物リストメニューを表示・実行"""
        while True:
            print("\n" + "-"*30)
            print("    買い物リスト管理")
            print("-"*30)
            print("1. アイテム追加")
            print("2. アイテム削除")
            print("3. アイテム完了")
            print("4. リスト表示")
            print("5. 合計金額計算")
            print("6. メインメニューに戻る")
            
            try:
                choice = input("\n選択してください (1-6): ").strip()
                
                if choice == "1":
                    self.add_item_to_list()
                elif choice == "2":
                    self.remove_item_from_list()
                elif choice == "3":
                    self.complete_item_in_list()
                elif choice == "4":
                    self.display_shopping_list()
                elif choice == "5":
                    self.calculate_total_cost()
                elif choice == "6":
                    break
                else:
                    print("無効な選択です")
            except KeyboardInterrupt:
                print("\n操作がキャンセルされました")
                break
    
    def add_item_to_list(self):
        """アイテムをリストに追加"""
        try:
            item_name = input("アイテム名を入力: ").strip()
            if not item_name:
                print("アイテム名は必須です")
                return
            
            quantity_str = input("数量を入力 (デフォルト: 1): ").strip()
            quantity = int(quantity_str) if quantity_str else 1
            
            price_str = input("価格を入力 (任意、円): ").strip()
            price = float(price_str) if price_str else None
            
            message = self.shopping_list.add_item(item_name, quantity, price)
            print(message)
        except ValueError:
            print("数量または価格の形式が無効です")
        except Exception as e:
            print(f"エラー: {e}")
    
    def remove_item_from_list(self):
        """アイテムをリストから削除"""
        try:
            self.display_shopping_list()
            items = self.shopping_list.get_items()
            if not items:
                print("削除するアイテムがありません")
                return
            
            index_str = input("削除するアイテム番号を入力: ").strip()
            index = int(index_str) - 1
            message = self.shopping_list.remove_item(index)
            print(message)
        except (ValueError, IndexError) as e:
            print(f"エラー: {e}")
        except Exception as e:
            print(f"エラー: {e}")
    
    def complete_item_in_list(self):
        """アイテムを完了済みに移動"""
        try:
            self.display_shopping_list()
            items = self.shopping_list.get_items()
            if not items:
                print("完了するアイテムがありません")
                return
            
            index_str = input("完了するアイテム番号を入力: ").strip()
            index = int(index_str) - 1
            message = self.shopping_list.complete_item(index)
            print(message)
        except (ValueError, IndexError) as e:
            print(f"エラー: {e}")
        except Exception as e:
            print(f"エラー: {e}")
    
    def display_shopping_list(self):
        """買い物リストを表示"""
        items = self.shopping_list.get_items()
        completed_items = self.shopping_list.get_completed_items()
        
        print("\n=== 買い物リスト ===")
        
        if items:
            print("【未完了アイテム】")
            for i, item in enumerate(items, 1):
                price_str = f" - ¥{item['price']}" if item['price'] else ""
                print(f"{i}. {item['name']} (数量: {item['quantity']}){price_str}")
        else:
            print("未完了アイテムはありません")
        
        if completed_items:
            print("\n【完了済みアイテム】")
            for item in completed_items:
                price_str = f" - ¥{item['price']}" if item['price'] else ""
                print(f"✓ {item['name']} (数量: {item['quantity']}){price_str}")
    
    def calculate_total_cost(self):
        """合計金額を計算・表示"""
        total = self.shopping_list.calculate_total()
        if total > 0:
            print(f"\n価格設定済みアイテムの合計金額: ¥{total}")
        else:
            print("\n価格が設定されたアイテムがありません")
    
    def save_list(self):
        """リストをファイルに保存"""
        try:
            filename = input("保存ファイル名を入力 (.txt): ").strip()
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            message = self.shopping_list.save_to_file(filename)
            print(message)
        except Exception as e:
            print(f"保存エラー: {e}")
    
    def load_list(self):
        """ファイルからリストを読み込み"""
        try:
            filename = input("読み込みファイル名を入力: ").strip()
            message = self.shopping_list.load_from_file(filename)
            print(message)
        except Exception as e:
            print(f"読み込みエラー: {e}")
    
    def run(self):
        """アプリケーションのメインループ"""
        print("買い物リスト & 電卓アプリケーションを開始します")
        
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
    """メイン関数"""
    app = ShoppingCalculatorApp()
    app.run()


if __name__ == "__main__":
    main()