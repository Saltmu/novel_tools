# Novel Tools

「重天の調律師」シリーズの執筆・校閲・フォーマットを支援するエージェント環境です。

## プロジェクト構成

```
novel_tools/
├── novels/                   # 執筆済み小説テキスト（章-話.txt 形式）
├── novel_check_results/      # レビュー結果の保存先（章-話ごとのサブフォルダ）
├── data/sources/             # 執筆参照資料（設定資料集・プロット・キャラ概要）
├── skills/                   # エージェントスキル群
└── .agents/workflows/        # 定義済みワークフロー
```

## スキル構成

本プロジェクトには、小説執筆をサポートする **9つのエージェントスキル** が用意されています。エージェントに指示を出す際は、各スキルの**キーワード**を添えて呼び出してください。

### 1. Writing（執筆）

- **Novel-Writer** [`novel-writer`]
  「重天の調律師」シリーズの専属作家スキル。設定資料・キャラクター概要・プロットに基づき、執筆ポリシーを厳守して小説を生成する。章単位の執筆指示を受け、エピソードごとに執筆して `novels/` フォルダに保存する。

### 2. Formatting（フォーマット調整）

- **Novel-Formatter** [`novel-formatter`]
  執筆された小説テキストを、ウェブ小説（カクヨム、なろう等）向けに読みやすくフォーマットする。機械的な前処理とAIによる文脈的調整の2段階で処理する。

### 3. Core Verification（基本検証）

- **World-Logic-Guard** [`world-logic-guard`]
  独自の世界観設定（物理法則、地理、エネルギー体系）との論理的整合性を検証する。
- **Consistency-Checker** [`consistency-checker`]
  執筆中の最新シーンと、過去のプロット・キャラ設定との矛盾を検出する。

### 4. Quality Enhancement（品質向上）

- **Show-Dont-Tell-Enhancer** [`show-dont-tell-enhancer`]
  「説明」を「体験」に変え、読者の感情を揺さぶる描写を提案する。
- **Foreshadowing-Tracker** [`foreshadowing-tracker`]
  伏線と情報開示のタイミングを追跡し、カタルシスを最大化する。
- **Plot-Pacing-Analyzer** [`plot-pacing-analyzer`]
  プロットと本文を比較し、物語の進行速度や文字数の比重を分析する。
- **Rhythm-Vocabulary-Optimizer** [`rhythm-vocabulary-optimizer`]
  文章のリズムと語彙を最適化し、読みやすさと表現の豊かさを向上させる。
- **Character-Voice-Checker** [`character-voice-checker`]
  キャラクターの口調のブレと感情導線の自然さをチェックする。

## ワークフロー

### `/novel_review_pipeline`

フォーマット → 7並列レビューを、複数ファイルにまたがって一括実行するワークフローです。`novels/` フォルダ内の全 `.txt` ファイルを対象に、以下の処理を自動で行います。

1. `novel-formatter` でフォーマット → `novel_check_results/[ファイル名]/01_formatted.txt` に保存
2. 以下の7スキルを**並列実行**してレビューレポートを生成：

| ファイル名              | スキル                      |
| ----------------------- | --------------------------- |
| `02_world_logic.md`     | world-logic-guard           |
| `03_consistency.md`     | consistency-checker         |
| `04_show_dont_tell.md`  | show-dont-tell-enhancer     |
| `05_foreshadowing.md`   | foreshadowing-tracker       |
| `06_pacing.md`          | plot-pacing-analyzer        |
| `07_rhythm.md`          | rhythm-vocabulary-optimizer |
| `08_character_voice.md` | character-voice-checker     |

```
# 使用例：エージェントへの依頼
「/novel_review_pipeline を使って novels/ 内の全ファイルをレビューして」
```

## 参照資料（data/sources/）

| ファイル                          | 内容                                 |
| --------------------------------- | ------------------------------------ |
| `00_執筆ポリシーver.2.txt`        | 文体・ルビ・描写ルール等の執筆方針   |
| `01_重天の調律師_設定資料集.txt`  | 世界観・魔法体系・地理等の設定資料集 |
| `02_創世記から現代まで.txt`       | 世界の歴史年表                       |
| `03-1_第１幕キャラクター概要.txt` | 第1幕登場キャラクターの詳細          |
| `04-1_第1幕プロットver.2.txt`     | 第1幕の詳細プロット                  |
| `04_大枠プロット.txt`             | シリーズ全体の大枠プロット           |

## セットアップ

### 1. 仮想環境の作成と依存関係のインストール

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
