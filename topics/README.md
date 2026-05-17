# `topics/` ディレクトリ

メイン README のチェックリストに対応させた実験置き場。パスは英語の **`snake_case`** を使う。

## 雛形の生成

親トピックのパスと日本語／英語タイトルは [`scripts/topic_manifest.json`](../scripts/topic_manifest.json) が一次情報（下の一覧表と同期させる）。子トピックはマニフェストの `children` に列挙したうえで `create-all --children` でまとめて作るか、単発では `create` にフルパスを渡す。

リポジトリルートから（例）:

```bash
uv run python scripts/scaffold_topics.py list
uv run python scripts/scaffold_topics.py create-all           # 親トピックのみ
uv run python scripts/scaffold_topics.py create-all --children # 親 + manifest の children
uv run python scripts/scaffold_topics.py create advanced/nlp/my_experiment --title-ja "独自実験"
uv run python scripts/scaffold_topics.py --dry-run create-all  # 書き換え確認のみ
```

既存の `README.md` / `data/README.md` は既定ではスキップする。テンプレに戻したいときだけ **`--force`**（注意して使う）。

## 各トピックの中身（おすすめ）

```
<topic>/
├── README.md        # 何を試したか、データの入手先、実行コマンド
├── notebooks/       # Jupyter / marimo など（任意）
├── src/             # `.py` スクリプト（任意）
├── data/            # 生データ（Git 無視、`data/README.md` のみ追跡可）
└── outputs/         # 図・ログ・小さめの評価結果（肥大化したらここごと無視検討）
```

`artifacts/` が必要になったら同階層で追加してよい（チェックポイント等）。既定では `.gitignore` で `outputs/` と `artifacts/` を無視している。

## スキルツリー → パス対応（太字見出し = ひとつのトピック）

### 1. 伝統的機械学習 (`traditional_ml/`)

| チェックリストの塊 | ディレクトリ |
|-------------------|----------------|
| 回帰 | `traditional_ml/regression/` |
| 分類 | `traditional_ml/classification/` |
| アンサンブル | `traditional_ml/ensemble/` |
| 教師なし | `traditional_ml/unsupervised/` |
| モデル評価・検証 | `traditional_ml/evaluation/` |

### 2. 深層学習の基礎 (`deep_learning/`)

| チェックリストの塊 | ディレクトリ |
|-------------------|----------------|
| 基本アーキテクチャ | `deep_learning/mlp_and_optimization/` |
| 画像処理の基礎 (CV) | `deep_learning/vision_basics/` |
| 系列データの基礎 | `deep_learning/sequences/` |

### 3. 応用 (`advanced/`)

| チェックリストの塊 | ディレクトリ |
|-------------------|----------------|
| NLP ルート | `advanced/nlp/` |
| CV ルート | `advanced/cv/` |
| GNN ルート | `advanced/gnn/` |
| CV × GNN 融合ルート | `advanced/cv_and_gnn/` |
| マルチモーダル | `advanced/multimodal/` |
| その他の専門ルート | `advanced/special_topics/` |

大きくなったら、その下にだけサブフォルダを切る（例: `advanced/nlp/rag_app/`）。

### 4. MLOps (`mlops/`)

| チェックリストの塊 | ディレクトリ |
|-------------------|----------------|
| Web API 化 | `mlops/web_and_demo/` |
| 実験管理・運用 | `mlops/experiment_and_deploy/` |

### 5. 理論・数学 (`math_theory/`)

ノート中心ならフラットでもよい。

| チェックリストの塊 | ディレクトリ（例） |
|-------------------|-------------------|
| 線形代数 / 微積分 / 確率統計 | `math_theory/` 直下に `linear_algebra.ipynb` のようにファイルを並べる、または必要なら `math_theory/<名前>/` で分割 |
