### 学習の進め方

トップダウン型で進める、**このリストを上から順に埋める必要はない**

### 🐍 Python 環境（uv）

- **基本方針**: リポジトリのルートに `uv` のプロジェクトを **1つ**（`pyproject.toml` と `uv.lock`）置く。
- **コードやノート**はトピックごとのサブディレクトリに分けてよいが、依存関係が大きく食い違わない限りは **共通の環境のまま**で進める。
- **例外的に分けるとき**: パッケージのバージョンが衝突する、または章・実験ごとに lock を固定して再現性を切り離したい — そのときだけ、そのディレクトリ配下に別の `uv` プロジェクトを用意する。

### 📁 トピックの粒度・ディレクトリ・データ

- **粒度（デフォルト）**: チェックリストの **太字の塊ひとつ = `topics/` 以下のひとつのトピックディレクトリ** とする（例:「回帰」なら線形・Ridge・Lasso は同じトピックにまとめてよい）。
- **さらに分けるとき**: 子チェック項目が単独で「数日〜」の自作実験サイズまで育ったら、その下に **`snake_case` のサブディレクトリ**を増やす（例: `topics/advanced/nlp/bert_classifier/`）。
- **配置場所**: 実験用のコード・ノート・ログはすべて対応する `topics/<大分類>/<トピック>/` の下へ。対応関係の一覧は [`topics/README.md`](topics/README.md) を見る。
- **データ**: 生データ・中間生成物・学習済み重みは **Git に置かない**（取得元 URL、`uv run …` での準備コマンドを各トピックの `README.md` または `data/README.md` に書く）。リポジトリ直下の共通データ置き場は設けず、基本的にトピック横に並べない。
- **雛形の自動生成**: [`scripts/scaffold_topics.py`](scripts/scaffold_topics.py) が `README.md`・`data/README.md`・`notebooks/`・`src/`・`outputs/` をまとめて用意する（既存ファイルは既定では上書きしない）。親トピックの一覧・タイトルは [`scripts/topic_manifest.json`](scripts/topic_manifest.json)。使い方の詳細は [`topics/README.md`](topics/README.md) の「雛形の生成」。

```bash
# 一覧
uv run python scripts/scaffold_topics.py list

# マニフェストの親トピックをまとめて作成
uv run python scripts/scaffold_topics.py create-all

# 任意のパス（子トピック含む snake_case は / でつなぐ）
uv run python scripts/scaffold_topics.py create advanced/nlp/rag_demo
```

ひな形の手編集例として [`topics/traditional_ml/regression/`](topics/traditional_ml/regression/README.md) もある。

### 🗺️ 機械学習 スキルツリー＆進捗マップ

#### 1. 🌳 伝統的機械学習 (Traditional ML)

- [ ] **回帰 (数値の予測)**
    - [ ] 線形回帰 (Linear Regression)
    - [ ] リッジ回帰 / ラッソ回帰 (正則化の理解)


- [ ] **分類 (カテゴリの予測)**
    - [ ] ロジスティック回帰 (Logistic Regression)
    - [ ] 決定木 (Decision Tree)
    - [ ] SVM (サポートベクターマシン)


- [ ] **アンサンブル学習 (Kaggle等での最強手法)**
    - [ ] ランダムフォレスト (Random Forest)
    - [ ] 勾配ブースティング木 (XGBoost / LightGBM)


- [ ] **教師なし学習**
    - [ ] K-Means (クラスタリング)
    - [ ] PCA (主成分分析による次元削減)


- [ ] **モデル評価・検証**
    - [ ] 交差検証 (Cross Validation)
    - [ ] 評価指標の理解 (Accuracy, Precision, Recall, F1, RMSE)



#### 2. 🧠 深層学習の基礎 (Deep Learning Basics)

- [ ] **基本アーキテクチャ**
    - [ ] 全結合ニューラルネットワーク (MLP / FNN)
    - [ ] 誤差逆伝播法と最適化アルゴリズム (SGD, Adamなど)


- [ ] **画像処理の基礎 (CV)**
    - [ ] CNN (畳み込みニューラルネットワーク)
    - [ ] 転移学習 / ファインチューニング (ResNetなどの学習済みモデルの利用)


- [ ] **系列データの基礎 (NLP / 時系列)**
    - [ ] RNN / LSTM / GRU
    - [ ] Word2Vec / Embedding (単語のベクトル化)



#### 3. 🚀 応用タスク・最前線 (Advanced & Generative AI)

- [ ] **自然言語処理 (NLP) ルート**
    - [ ] Transformer の仕組み理解
    - [ ] BERT を用いたテキスト分類・固有表現抽出
    - [ ] LLM (大規模言語モデル) のプロンプトエンジニアリング
    - [ ] LLM のファインチューニング (LoRA / PEFT)
    - [ ] RAG (検索拡張生成) アプリケーションの実装

- [ ] **コンピュータビジョン (CV) ルート**
    - [ ] 物体検出 (YOLO シリーズの実装)
    - [ ] セマンティックセグメンテーション (U-Netなど)
    - [ ] 画像生成 (GAN / 拡散モデル: Stable Diffusionの操作・微調整)

- [ ] **グラフニューラルネットワーク（GNN）ルート**
    - [ ] PyTorch Geometricの基礎

- [ ] **$CV \times GNN$融合ルート**
    - [ ] シーングラフ生成(SGG)
        - [ ] 画像からのオブジェクト・関係性の同時抽出

- [ ] **マルチモーダル (Multimodal) ルート**
    - [ ] CLIP等のモデルを使った画像・テキストの連携処理
    - [ ] VQA (画像に対する質疑応答) の実装
    - [ ] オープンソースVLM (LLaVAなど) のファインチューニング

- [ ] **その他の専門ルート**
    - [ ] 強化学習 (Q-Learning, DQN)
    - [ ] 音声認識・合成 (Whisper等の利用)
    - [ ] 推薦システム (協調フィルタリングなど)
    - [ ] GNN


#### 4. ⚙️ 実運用・MLOps (Deployment & MLOps)

- [ ] **Web API化**
    - [ ] FastAPI / Flask 等によるモデルのAPI化
    - [ ] Streamlit / Gradio によるデモUIの爆速作成


- [ ] **実験管理・運用**
    - [ ] MLflow / Weights & Biases による学習記録の管理
    - [ ] クラウドへのデプロイ (AWS / GCP / Azure の基礎)


#### 5. 📐 理論・数学 (Math & Theory) ※壁にぶつかったら戻る場所

- [ ] **線形代数** (ベクトル、行列の掛け算、固有値)
- [ ] **微積分** (偏微分、合成関数の微分・連鎖律)
- [ ] **確率・統計** (正規分布、ベイズの定理、最尤推定)
