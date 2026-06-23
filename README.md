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

本プロジェクトには、小説執筆をサポートする **12のエージェントスキル** が用意されています。エージェントに指示を出す際は、各スキルの**キーワード**を添えて呼び出してください。

### 1. Writing（執筆）

- **Novel-Writer** [`novel-writer`]
  「重天の調律師」シリーズの専属作家スキル。設定資料・キャラクター概要・プロットに基づき、執筆ポリシーを厳守して小説を生成する。章単位の執筆指示を受け、エピソードごとに執筆して `novels/` フォルダに保存する。
- **Novel-Writer (Antigravity CLI版)** [`novel_writer_antigravitycli`]
  Antigravity CLI環境との連携に最適化された小説執筆スキル。

### 2. Formatting（フォーマット調整）

- **Novel-Formatter** [`novel-formatter`]
  執筆された小説テキストを、ウェブ小説（カクヨム、なろう等）向けに読みやすくフォーマットする。機械的な前処理とAIによる文脈的調整の2段階で処理する。

### 3. Core Verification（基本検証）

- **World-Logic-Guard** [`world-logic-guard`]
  独自の世界観設定（物理法則、地理、エネルギー体系）との論理的整合性を検証する。
- **Consistency-Checker** [`consistency-checker`]
  執筆中の最新シーンと、過去のプロット・キャラ設定との矛盾を検出する。
- **Logic-Consistency-Reviewer (統合レビュー)** [`logic-consistency-reviewer`]
  世界観設定、過去のプロット・キャラクター設定との矛盾、伏線の配置を統合的かつ包括的に検証する。

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
- **Style-Expression-Reviewer (統合レビュー)** [`style-expression-reviewer`]
  描写力（Show, Don't Tell）、文章のリズム・語彙、キャラクターの口調、構成（ペーシング）を統合的に検証する。

## ワークフローとマルチエージェントレビュー

包括的な小説レビューを実行するために、本プロジェクトは**「マルチエージェント（設定監査＆文芸表現）」**による並列レビューと、LLMによる自動競合解消（マージ）を採用しています。

### 1. エージェントチャットでの実行 (`/novel_review_pipeline`)

エージェントとの対話型ワークフローです。`novels/` フォルダ内の指定された小説ファイルを対象に、以下の手順を行います。

1. **前処理**: `novel-formatter` によるフォーマット整形と、`filter_context.py` による関連設定情報の事前抽出。
2. **サブエージェント並列レビュー**: 
   メインエージェントが2つの専門サブエージェントを並列で起動します：
   * **設定監査エージェント (Logic Auditor)**: `logic-consistency-reviewer` を使用し、設定やプロットとの矛盾、伏線の配置を検証します。
   * **文芸表現エージェント (Style Editor)**: `style-expression-reviewer` を使用し、描写力・リズム・口調・ペーシングを検証します。
3. **編集長による統合 (マージ＆競合解消)**:
   メインエージェントが双方の指摘結果を分析し、**重複の排除**および**「表現の提案が世界観設定（ロジック）と衝突していないか」の自動調整**を行い、統合された唯一の指摘ファイル `00_integrated_findings.yaml` と、概要レポート `00_integrated_report.md` を出力します。
4. **人間レビュー**: `00_integrated_findings.yaml` 内の指摘を確認し、適用したい項目について `accepted: "n"` から `accepted: "y"` に変更します。
5. **自動反映**: YAML編集後、エージェントに以下のプロンプトを送信して修正を一括反映します：
   ```
   「novel_check_results/[フォルダ名]/00_integrated_findings.yaml を読み取り、accepted: "y" の指摘を 01_formatted.txt に反映して」
   ```

---

### 2. コマンドライン（Pythonスクリプト）での実行

ローカルのターミナルから直接レビュープロセス（並列レビューからLLM統合まで）を全自動で実行するスクリプトです。

```bash
# 特定の章をレビューする場合
poetry run python src/run_review_pipeline.py novels/1_12.txt

# 使用するモデルを指定する場合 (デフォルト: Gemini 3.5 Flash (High))
poetry run python src/run_review_pipeline.py novels/1_12.txt --model "Gemini 3.5 Flash (High)"
```

実行が完了すると、`novel_check_results/[ファイル名]/` 配下に以下のファイルが自動生成されます：
* `01_formatted.txt`: 整形済み小説本文
* `02_logic_consistency.yaml`: 設定監査エージェントの指摘（中間ファイル）
* `03_style_expression.yaml`: 文芸表現エージェントの指摘（中間ファイル）
* `00_integrated_findings.yaml`: **LLMによって競合解消・マージされた最終的な指摘YAML**
* `00_integrated_report.md`: 人間向けの見やすいマークダウンレポート

生成後、**「人間レビュー」**（`00_integrated_findings.yaml` の `accepted: "y"` への変更）を行い、上記のエージェント指示、または後述の反映コマンドで小説へ反映します。

---

#### レビュー結果のYAML構造

統合された指摘は以下の共通スキーマに従って出力されます：

```yaml
findings:
  - id: "INT-001"              # 統合(Integrated)を示すID＋連番
    location: "8行目"          # 該当箇所
    original: "「原文の抜粋」"  # 対象テキスト
    category: "設定矛盾"       # 指摘のカテゴリ
    severity: "high"           # high / medium / low / info
    analysis: "競合が解消された分析・理由の詳細"
    suggestion: "設定を考慮して調整された修正提案"
    accepted: "n"              # ← "y" に変更すると採用
```

#### 使い方

##### 1. エージェントチャットでの対話的反映

1. **レビューの実行**:
   チャットに以下の指示を送信して並列レビューを実行します。
   ```
   /novel_review_pipeline を使って novels/1_12.txt をレビューして
   ```
2. **対話的反映の実行**:
   レビュー完了後、エージェントが統合された指摘の一覧を提示し、反映するかどうかを問いかけます。
   - 「`INT-001` と `INT-003` を適用して」、「すべて適用して」、「不要」などのようにチャットで返答するだけで、エージェントが自動的にスクリプトを呼び出して小説テキスト（`01_formatted.txt`）に修正を正確に適用します。

##### 2. コマンドライン（CLI）での対話的・自動反映

ローカルのターミナルからスクリプトを直接実行し、対話的または自動で反映を行うことができます。

```bash
# ターミナル上で1件ずつ確認しながら反映する（手動修正入力も可能）
poetry run python src/apply_findings.py --dir novel_check_results/1_12 --interactive

# 手動でYAMLを編集して accepted: "y" にしたものを一括自動反映する
poetry run python src/apply_findings.py --dir novel_check_results/1_12 --auto

# 特定の指摘ID（カンマ区切り）だけを指定して反映する
poetry run python src/apply_findings.py --dir novel_check_results/1_12 --accept-ids INT-001,INT-003

# LLMを使用せず、指摘内容の「...」から修正文字列を抽出して単純置換する
poetry run python src/apply_findings.py --dir novel_check_results/1_12 --auto --no-llm
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
