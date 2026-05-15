# 武豊町 財政分析API

武豊町の予算書・決算書などの公開財政資料を自動取得し、AIを活用して分析・可視化するAPIです。
住民・納税者の財政監視と民主的監視を支援します。

## 機能

### 1. 自動データ取得
- 武豊町公式ウェブサイトから予算書・決算書を定期的に自動ダウンロード
- PDF・Excel形式に対応
- GitHub Actions で定期実行

### 2. AI分析エンジン（OpenAI GPT-4.5）
- **予算配分の不適切さ検出** - 異常な支出パターンを自動検知
- **年度間の支出傾向分析** - 複数年度の比較分析
- **特定部門の異常支出検警** - 部門別の詳細異常検知
- **支出内容の自動要約** - 原文資料から要点を抽出

### 3. 原文トレーサビリティ
- AI分析結果が元資料のどこを参照したか記録
- 原文との照合検証が可能

## システム構成

```
taketo-financial-api/
├── .github/workflows/     # GitHub Actions 定期実行設定
├── src/
│   ├── scraper.py        # データ取得・スクレイピング
│   ├── analyzer.py       # AI分析エンジン（GPT-4.5）
│   ├── api.py           # FastAPI サーバー
│   └── utils.py         # ユーティリティ
├── data/                 # ダウンロード済み資料
├── reports/              # 分析レポート出力
├── requirements.txt      # Python依存パッケージ
└── .env.example         # 環境変数テンプレート
```

## セットアップ

### 1. 前提条件
- Python 3.9+
- OpenAI API キー
- Git

### 2. インストール

```bash
git clone https://github.com/kiinoneko/taketo-financial-api.git
cd taketo-financial-api
pip install -r requirements.txt
```

### 3. 環境設定

```bash
cp .env.example .env
# .env を編集して OpenAI API キーを設定
nano .env
```

### 4. 実行

```bash
# API サーバー起動
python -m uvicorn src.api:app --reload

# 手動でデータ取得・分析実行
python src/scraper.py
python src/analyzer.py
```

## API エンドポイント

### データ取得
```
GET /api/v1/download
```
最新の予算書・決算書をダウンロード

### 分析結果取得
```
GET /api/v1/analysis?year=2024
```
AI分析結果（異常検知、傾向分析、要約など）

### レポート生成
```
POST /api/v1/report
```
分析レポートをJSON形式で生成

## 使用方法

### 1. 初回セットアップ
```bash
python src/scraper.py  # 武豊町サイトから資料取得
```

### 2. AI分析実行
```bash
python src/analyzer.py  # GPT-4.5で自動分析
```

### 3. レポート確認
分析結果は `reports/` ディレクトリに出力されます

## 自動実行スケジュール

GitHub Actions で以下のスケジュールで自動実行：
- **毎月末** - 新しい財政資料の取得
- **毎日** - AI分析の実行とレポート生成

## 分析内容詳細

### 予算配分の不適切さ検出
- 過去年度との比較で異常な支出増減を検知
- 予算配分の効率性をスコア化

### 年度間の支出傾向分析
- 複数年度の支出パターン変化を可視化
- トレンド予測

### 特定部門の異常支出検警
- 各部門（福祉、教育、土木など）の異常を検知
- 根拠となる原文資料を自動参照

### 支出内容の自動要約
- 複雑な予算書から要点を抽出
- 納税者向けの分かりやすい説明文を生成

## トレーサビリティ

すべての分析結果には以下の情報が含まれます：
- 参照した原文資料（ファイル名、ページ番号）
- 根拠となるデータ箇所
- 分析根拠の詳細説明

これにより、原文との照合検証が可能です。

## ライセンス

MIT License

## 貢献

このプロジェクトは納税者の権利擁護と民主的な財政監視を目的としています。
改善提案やバグ報告は Issues にお願いします。

## 注記

このAPIは公開情報に基づき自動分析を行いますが、最終的な判断は原文資料の確認に基づいて行ってください。
