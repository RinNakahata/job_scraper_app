# 求人ボックス スクレイピング Webアプリ

このプロジェクトは、Flask + Playwright + Pandas を使用して、[求人ボックス](https://xn--pckua2a7gp15o89zb.com)から求人情報をスクレイピングし、ExcelファイルとしてダウンロードできるWebアプリです。

---

## 🔧 使用技術

- Python 3.x
- Flask
- Playwright（非同期処理）
- Pandas（Excel出力用）
- HTML + CSS（スタイリング）


## 📂 ディレクトリ構成

```
project-root/
├── app.py                # Flaskアプリケーション
├── scraper/
│   └── job_scraper.py    # Playwrightを用いたスクレイピングロジック
├── templates/
│   └── index.html        # フロントエンド（HTMLフォーム）
├── output/
│   └── 求人情報一覧.xlsx   # スクレイピング結果（自動生成）
└── README.md
```


## 🚀 セットアップ手順

1. **リポジトリをクローン**
```bash
git clone https://github.com/your-username/jobbox-scraper.git
cd jobbox-scraper
```

2. **仮想環境を作成して有効化**
```bash
python -m venv venv
source venv/bin/activate   # (Windowsの場合: venv\Scripts\activate)
```

3. **依存パッケージをインストール**
```bash
pip install -r requirements.txt
```

4. **Playwrightのインストール**
```bash
python -m playwright install
```

5. **アプリを起動**
```bash
python app.py
# ローカルホストで起動 → http://127.0.0.1:5000 にアクセス
```


## 🖥️ 使い方

1. フォームに以下の条件を入力:
   - キーワード（例: プログラマー）  
   - 勤務地（例: 東京都）  
   - 雇用形態（プルダウンで選択）

2. 「スクレイピング実行」ボタンをクリック

3. 完了後、自動でExcelファイル（求人情報一覧.xlsx）がダウンロード可能になります。


## 💼 取得項目

- 求人タイトル  
- 企業名  
- 所在地  
- 給与  
- 雇用形態


## 📌 雇用形態の対応値

| 雇用形態 | 値 |
|----------|----|
| 正社員             | 1 |
| アルバイト・パート | 2 |
| 派遣社員           | 3 |
| 契約・臨時・期間   | 4 |
| 業務委託           | 5 |
| 新卒・インターン   | 6 |


## ⚠️ 注意事項

- Playwrightは非同期処理で動作するため、環境によっては動作に多少時間がかかります。
- 本アプリは求人ボックスのHTML構造に依存しているため、構造が変更された場合はセレクタを更新してください。



## ✍ 作者
- 名前：Rin Nakahata
- 技術ブログ（note）：[note記事はこちら](https://note.com/rin_nakahata/n/na7f794af51f6)



## 📝 ライセンス

MITライセンスです。自由にご利用・改変・再配布いただけます。
