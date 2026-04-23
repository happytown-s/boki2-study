# Boki 2 Study

> 日商簿記2級（Level 2 Bookkeeping）試験対策のWebアプリケーション

## Features

- 科目別クイズ -- 10の会計分野から出題
- 計算トレーニング -- 減価償却・製造原価・プロセス原価計算
- 科目B（午後）演習 -- 複合的な会計サイクル問題
- 学習進捗管理 -- localStorageによる解答履歴の記録
- ダークテーマUI -- 青系アクセントのダークスキーム

## Contents

### Quiz（科目別クイズ）
- 全280問（10カテゴリ）
- カテゴリ一覧（問題数）:
  - Advanced Journal Entries: 43
  - Corporation Accounting: 33
  - Product Costing: 33
  - Overhead（製造間接費）: 31
  - Financial Statements: 27
  - Materials（材料費）: 28
  - Depreciation & Fixed Assets: 25
  - Labor（労務費）: 25
  - Partnership: 20
  - Error Correction: 15
- クイズモード: カテゴリ選択、ランダム出題、解説表示

### Calc Training（計算トレーニング）
- 全77問（3ファイル）
- 減価償却の計算: 26問
- 製造原価報告書（COGM）: 25問
- 総合計算（プロセス原価計算、企業会計、財務比率、組合会計）: 26問

### Subject B（科目B演習）
- 27問
- カテゴリ一覧（問題数）:
  - Complete Accounting Cycle: 10
  - Complex Journal Entries: 5
  - Manufacturing Cost Flow: 5
  - Statement Preparation: 4
  - Error Analysis: 3

### Progress（進捗管理）
- 解答履歴と正答率の確認

## Tech Stack

- React 19 + TypeScript
- Vite（ビルドツール）
- Tailwind CSS（スタイリング）
- localStorage（進捗データ永続化）

## Usage

```bash
npm install
npm run dev
```

ブラウザで `http://localhost:5173` にアクセス。

## Deployment

```bash
npm run build
```

`dist/` ディレクトリを任意の静的ホスティングサービスにデプロイ。

## License: MIT
