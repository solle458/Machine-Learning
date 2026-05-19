# GNN（グラフニューラルネットワーク）トピック

`advanced/gnn` の実験用ディレクトリ。

## データ

ローカルの `data/` に置く（Git には上げない）。入手元と前処理メモは [data/README.md](data/README.md) に書く。

## 実行例

リポジトリルートで（`uv` 利用時）:

```bash
cd topics/advanced/gnn
uv run python main.py
```

リポジトリルートから直接実行しても、データとログはこのディレクトリ配下に保存されます。

```bash
uv run python topics/advanced/gnn/main.py
```

### CLI オプション

| オプション | 既定 | 説明 |
|-----------|------|------|
| `--dataset` | `pubmed` | `cora` / `pubmed` / `citeseer` |
| `--epochs` | `200` | 学習エポック数 |
| `--log-level` | `INFO` | コンソールのログレベル |
| `--info` | off | 学習前にグラフ要約をログ出力 |
| `--visualize` | off | 学習前にグラフを表示 |

例:

```bash
uv run python main.py --dataset cora --info
```

## テスト

```bash
cd topics/advanced/gnn
uv run pytest
```
