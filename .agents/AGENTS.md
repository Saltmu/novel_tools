# Antigravity 開発・運用ルール

本プロジェクトにおいて、Antigravityが作業およびユーザーとのやり取りを行う際は、以下のルールを遵守してください。

## 1. ユーザーとのやり取りについて
- **日本語でのコミュニケーションの徹底**:
  ユーザーとの対話、作業報告、質問、および提案は、特別な指示がない限りすべて日本語で行ってください。

## 2. PowerShellコマンドの実行と文字コード
- **コンソール出力のUTF-8化**:
  PowerShellコマンドを実行する（`run_command`を使用する）際は、出力の文字化けを防ぐため、コマンドの先頭に必ず `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8;` をプレフィックスとして付加してください。
  *例*: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; <実際のコマンド>`

- **ファイル入出力時のエンコーディング指定**:
  PowerShellコマンドを使用してファイルの読み書き（`Get-Content`、`Out-File`、`Set-Content`、リダイレクト `>` など）を行う際は、Windowsのデフォルトエンコーディング（Shift_JISやUTF-16）による文字化けを防ぐため、必ず明示的に `-Encoding utf8` などを指定してUTF-8で処理してください。

## 3. Pythonの実行環境について
- **Poetry環境の利用**:
  Pythonスクリプトを実行する際は、依存関係の不整合を防ぐため、グローバル環境ではなくPoetryを使用し、`poetry run python <script.py>` の形式で実行するか、あるいはプロジェクト内の仮想環境（`venv`）をアクティベートして実行してください。

## 4. 小説の執筆・レビュー時の設定資料参照
- **参照資料（`data/sources/`）への準拠**:
  小説の執筆、レビュー、修正適用などのすべての作業において、`data/sources/` 配下にある設定資料・プロット・キャラクター概要を最優先のソース（真実の基準）として参照してください。推測や独自の判断で世界観設定、歴史、キャラクターの口調・設定を捏造または逸脱させてはなりません。

## 5. YAMLレビューレポートの形式遵守
- **レビュー結果のスキーマと反映ルール**:
  `/novel_review_pipeline` などのレビュー結果を格納するYAMLファイルを生成・更新する際は、プロジェクト規定のスキーマ（`findings` 配下の `id`, `location`, `original`, `category`, `severity`, `analysis`, `suggestion`, `accepted` 等）を厳格に維持してください。
  指摘を小説テキストに自動反映する際は、ユーザーが `accepted: "y"` とマークした指摘のみを正確に反映し、`accepted: "n"` またはその他の項目は変更しないようにしてください。また、反映時は文脈の自然さや執筆ポリシーに留意してください。
