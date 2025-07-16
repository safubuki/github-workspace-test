#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
買い物リスト管理と電卓機能アプリケーション - デモスクリプト
Demo script for Shopping List Manager with Calculator Functionality
"""

from calculator import Calculator
from shopping_list import ShoppingList
from shopping_calculator import ShoppingCalculatorApp

def run_demo():
    """アプリケーションの機能をデモンストレーション"""
    print("="*60)
    print("    買い物リスト & 電卓アプリケーション - デモ")
    print("="*60)
    
    # 電卓機能のデモ
    print("\n🔢 電卓機能のデモ")
    print("-" * 30)
    calc = Calculator()
    
    # 基本計算
    print("基本計算:")
    print(f"  298 + 158 = {calc.add(298, 158)}")
    print(f"  1000 - 157 = {calc.subtract(1000, 157)}")
    print(f"  5 × 120 = {calc.multiply(5, 120)}")
    print(f"  2400 ÷ 8 = {calc.divide(2400, 8)}")
    
    # 式計算（税込み価格など）
    print("\n式計算（税込み価格計算など）:")
    print(f"  298 * 1.08 = {calc.calculate_expression('298 * 1.08')}")
    print(f"  (100 + 200 + 150) * 1.08 = {calc.calculate_expression('(100 + 200 + 150) * 1.08')}")
    
    print(f"\n計算履歴: {len(calc.get_history())} 件の計算を実行")
    
    # 買い物リスト機能のデモ
    print("\n🛒 買い物リスト機能のデモ")
    print("-" * 30)
    shopping = ShoppingList()
    
    # アイテム追加
    print("アイテム追加:")
    print(f"  {shopping.add_item('りんご', 3, 298)}")
    print(f"  {shopping.add_item('バナナ', 2, 158)}")
    print(f"  {shopping.add_item('牛乳', 1, 89)}")
    print(f"  {shopping.add_item('パン', 2, 120)}")
    print(f"  {shopping.add_item('卵', 1, 298)}")
    
    # リスト表示
    print("\n現在の買い物リスト:")
    items = shopping.get_items()
    for i, item in enumerate(items, 1):
        price_str = f" - ¥{item['price']}" if item['price'] else ""
        print(f"  {i}. {item['name']} (数量: {item['quantity']}){price_str}")
    
    print(f"\n合計金額: ¥{shopping.calculate_total()}")
    
    # アイテム完了
    print("\n買い物完了:")
    print(f"  {shopping.complete_item(0)}")  # りんご完了
    print(f"  {shopping.complete_item(1)}")  # バナナ完了（インデックスが変わるので1）
    
    # 最終リスト表示
    print("\n買い物完了後のリスト:")
    remaining_items = shopping.get_items()
    completed_items = shopping.get_completed_items()
    
    print("【未完了アイテム】")
    for i, item in enumerate(remaining_items, 1):
        price_str = f" - ¥{item['price']}" if item['price'] else ""
        print(f"  {i}. {item['name']} (数量: {item['quantity']}){price_str}")
    
    print("【完了済みアイテム】")
    for item in completed_items:
        price_str = f" - ¥{item['price']}" if item['price'] else ""
        print(f"  ✓ {item['name']} (数量: {item['quantity']}){price_str}")
    
    print(f"\n残りの合計金額: ¥{shopping.calculate_total()}")
    
    # ファイル保存・読み込みのデモ
    print("\n💾 ファイル操作のデモ")
    print("-" * 30)
    filename = "demo_shopping_list.json"
    print(f"  {shopping.save_to_file(filename)}")
    
    # 新しいインスタンスで読み込みテスト
    new_shopping = ShoppingList()
    print(f"  {new_shopping.load_from_file(filename)}")
    print(f"  読み込み後のアイテム数: {len(new_shopping.get_items())} (未完了)")
    print(f"  読み込み後の完了済み: {len(new_shopping.get_completed_items())} (完了済み)")
    
    # テキスト形式での出力もテスト
    text_filename = "demo_shopping_list.txt"
    print(f"  {new_shopping.export_to_text(text_filename)}")
    
    print("\n" + "="*60)
    print("デモが完了しました!")
    print("実際のアプリケーションを起動するには:")
    print("  python3 shopping_calculator.py")
    print("="*60)


if __name__ == "__main__":
    run_demo()