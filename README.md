# Novel Tools

小説の整合性、世界観の維持、およびフォーマットを支援するエージェント環境です。

## スキル構成

- **Consistency-Checker**: 既記述との矛盾を検出
- **World-Logic-Guard**: 世界観設定との整合性をチェック
- **Novel-Formatter**: ウェブ小説（なろう、カクヨム等）向けの自動成形

## セットアップ

### 1. 仮想環境の作成と依存関係のインストール

本プロジェクトでは Python 3.3 以降の標準機能である `venv` を使用して環境を構築することを推奨します。

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. 設定ファイルの準備

1. `antigravity.yaml.example` を `antigravity.yaml` にコピーします。
   ```bash
   cp antigravity.yaml.example antigravity.yaml
   ```
2. `antigravity.yaml` を編集し、`folder_id` や `auth_file` のパスを自身の環境に合わせて設定してください。
   > [!IMPORTANT]
   > `antigravity.yaml` には機密情報が含まれるため、Gitにはコミットしないよう `.gitignore` で設定されています。
