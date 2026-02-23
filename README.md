# Novel Tools

小説の整合性、世界観の維持、およびフォーマットを支援するエージェント環境です。

## スキル構成

本プロジェクトには、小説執筆をサポートする8つのエージェントスキルが用意されています。エージェントに指示を出す際は、各スキルの**キーワード**を添えて呼び出してください（例：「`consistency-checker` を使って、このテキストの矛盾を確認して」など）。

### 1. Core Verification (基本検証)
- **Consistency-Checker** [キーワード: `consistency-checker`]
  執筆中の最新シーンと、過去のプロット・キャラ設定との矛盾を検出する。
- **World-Logic-Guard** [キーワード: `world-logic-guard`]
  独自の世界観設定（物理法則、地理、エネルギー体系）との論理的整合性を検証する。

### 2. Formatting (フォーマット調整)
- **Novel-Formatter** [キーワード: `novel-formatter`]
  NotebookLM等で執筆された小説を、ウェブ小説（カクヨム、なろう等）向けに読みやすくフォーマットする。

### 3. Quality Enhancement (品質向上)
- **Character-Voice-Checker** [キーワード: `character-voice-checker`]
  キャラクターの口調のブレと感情導線の自然さをチェックする。
- **Plot-Pacing-Analyzer** [キーワード: `plot-pacing-analyzer`]
  プロットと本文を比較し、物語の進行速度や文字数の比重を分析する。
- **Show-Dont-Tell-Enhancer** [キーワード: `show-dont-tell-enhancer`]
  「説明」を「体験」に変え、読者の感情を揺さぶる描写を提案する。
- **Rhythm-Vocabulary-Optimizer** [キーワード: `rhythm-vocabulary-optimizer`]
  文章のリズムと語彙を最適化し、読みやすさと表現の豊かさを向上させる。
- **Foreshadowing-Tracker** [キーワード: `foreshadowing-tracker`]
  伏線と情報開示のタイミングを追跡し、カタルシスを最大化する。

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
