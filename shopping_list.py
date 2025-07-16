#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
買い物リスト管理モジュール
Shopping list management module with JSON-based persistence.
"""

import json
import os
from datetime import datetime


class ShoppingList:
    """買い物リスト管理機能を提供するクラス
    
    アイテムの追加、削除、完了管理、およびJSONファイルでの永続化を行います。
    Manages shopping list items with add, remove, complete operations and JSON persistence.
    """
    
    def __init__(self, auto_load_file="shopping_list.json"):
        """ShoppingListクラスの初期化
        
        Args:
            auto_load_file (str): 自動読み込みするJSONファイル名
        """
        self.items = []
        self.completed_items = []
        self.data_file = auto_load_file
        
        # 起動時に既存ファイルがあれば自動読み込み
        if os.path.exists(self.data_file):
            try:
                self.load_from_file(self.data_file)
            except:
                pass  # 読み込みエラーは無視（新規作成として扱う）
    
    def add_item(self, item, quantity=1, price=None):
        """アイテムをリストに追加
        
        Args:
            item (str): アイテム名
            quantity (int): 数量（デフォルト: 1）
            price (float, optional): 価格
            
        Returns:
            str: 追加完了メッセージ
        """
        item_data = {
            'name': item,
            'quantity': quantity,
            'price': price,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.items.append(item_data)
        self._auto_save()
        return f"'{item}'をリストに追加しました"
    
    def remove_item(self, index):
        """指定されたインデックスのアイテムを削除
        
        Args:
            index (int): 削除するアイテムのインデックス（0ベース）
            
        Returns:
            str: 削除完了メッセージ
            
        Raises:
            IndexError: インデックスが範囲外の場合
        """
        if 0 <= index < len(self.items):
            removed_item = self.items.pop(index)
            self._auto_save()
            return f"'{removed_item['name']}'をリストから削除しました"
        else:
            raise IndexError("無効なアイテム番号です")
    
    def complete_item(self, index):
        """アイテムを完了済みに移動
        
        Args:
            index (int): 完了するアイテムのインデックス（0ベース）
            
        Returns:
            str: 完了メッセージ
            
        Raises:
            IndexError: インデックスが範囲外の場合
        """
        if 0 <= index < len(self.items):
            completed_item = self.items.pop(index)
            completed_item['completed_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.completed_items.append(completed_item)
            self._auto_save()
            return f"'{completed_item['name']}'を完了しました"
        else:
            raise IndexError("無効なアイテム番号です")
    
    def get_items(self):
        """現在の未完了アイテムリストを取得
        
        Returns:
            list: 未完了アイテムのコピー
        """
        return self.items.copy()
    
    def get_completed_items(self):
        """完了済みアイテムを取得
        
        Returns:
            list: 完了済みアイテムのコピー
        """
        return self.completed_items.copy()
    
    def calculate_total(self):
        """価格が設定されている未完了アイテムの合計金額を計算
        
        Returns:
            float: 合計金額
        """
        total = 0
        for item in self.items:
            if item['price']:
                total += item['price'] * item['quantity']
        return total
    
    def save_to_file(self, filename):
        """リストをJSONファイルに保存
        
        Args:
            filename (str): 保存先ファイル名
            
        Returns:
            str: 保存完了メッセージ
            
        Raises:
            IOError: ファイル保存エラーの場合
        """
        try:
            data = {
                'items': self.items,
                'completed_items': self.completed_items,
                'saved_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return f"リストを '{filename}' に保存しました"
        except Exception as e:
            raise IOError(f"ファイル保存エラー: {e}")
    
    def load_from_file(self, filename):
        """JSONファイルからリストを読み込み
        
        Args:
            filename (str): 読み込み元ファイル名
            
        Returns:
            str: 読み込み完了メッセージ
            
        Raises:
            FileNotFoundError: ファイルが見つからない場合
            IOError: ファイル読み込みエラーの場合
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.items = data.get('items', [])
            self.completed_items = data.get('completed_items', [])
            
            return f"リストを '{filename}' から読み込みました"
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイル '{filename}' が見つかりません")
        except Exception as e:
            raise IOError(f"ファイル読み込みエラー: {e}")
    
    def export_to_text(self, filename):
        """リストを人間が読みやすいテキスト形式で出力
        
        Args:
            filename (str): 出力先ファイル名
            
        Returns:
            str: 出力完了メッセージ
            
        Raises:
            IOError: ファイル出力エラーの場合
        """
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
            
            return f"リストを '{filename}' にテキスト形式で出力しました"
        except Exception as e:
            raise IOError(f"ファイル出力エラー: {e}")
    
    def _auto_save(self):
        """データの自動保存（内部メソッド）
        
        アイテムの変更時に自動的にJSONファイルに保存します。
        """
        try:
            self.save_to_file(self.data_file)
        except:
            pass  # 自動保存エラーは無視