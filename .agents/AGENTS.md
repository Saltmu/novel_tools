# Antigravity 開発・運用ルール

本プロジェクトにおいて、Antigravityが作業およびユーザーとのやり取りを行う際は、以下のルールを遵守してください。

## 1. ユーザーとのやり取りについて
- **日本語でのコミュニケーションの徹底**:
  ユーザーとの対話、作業報告、質問、および提案は、特別な指示がない限りすべて日本語で行ってください。

## 2. PowerShellコマンドの実行と文字コード
- **コンソール出力のUTF-8化**:
  PowerShellコマンドを実行する（`run_command`を使用する）際は、出力の文字化けを防ぐため、コマンドの先頭に必ず `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8;` をプレフィックスとして付加してください。
  （※注意: 各コマンドの実行ツールは毎回独立した新しいPowerShellプロセスで起動されるため、セッションは共有されず、実行ごとに毎回このプレフィックスを付加する必要があります）
  *例*: `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; <実際のコマンド>`

- **ファイル入出力時のエンコーディング指定**:
  PowerShellコマンドを使用してファイルの読み書き（`Get-Content`、`Out-File`、`Set-Content`、リダイレクト `>` など）を行う際は、Windowsのデフォルトエンコーディング（Shift_JISやUTF-16）による文字化けを防ぐため、必ず明示的に `-Encoding utf8` などを指定してUTF-8で処理してください。

- **Windows環境でのGitおよびGitHub CLIのパスと認証設定**:
  Windows環境において `git` または `gh` コマンドを使用する際は、コマンドが見つからないエラーや、`git push` 等が資格情報の入力プロンプトで応答待ち（ハング）になるのを防ぐため、以下の対応を必ず行ってください。
  1. コマンド実行前に、セッションの一時的な環境変数 `PATH` に Git および GitHub CLI の標準インストールパスを追加してください。
     *追加コード*: `$env:PATH += ";C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI"`
  2. Git操作（特にプッシュ等）を行う前には、資格情報エラーを防ぐために `gh auth setup-git` を実行してください。
  
  *例（Gitプッシュ時のワンライナー）*:
  `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $OutputEncoding = [System.Text.Encoding]::UTF8; $env:PATH += ";C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI"; gh auth setup-git; git push origin <branch_name>`

## 3. Pythonの実行環境について
- **Poetry環境の利用**:
  Pythonスクリプトを実行する際は、依存関係の不整合を防ぐため、グローバル環境ではなくPoetryを使用し、`poetry run python <script.py>` の形式で実行するか、あるいはプロジェクト内の仮想環境（`venv`）をアクティベートして実行してください。

## 4. 小説の執筆・レビュー時の設定資料参照
- **参照資料（`data/sources/`）への準拠**:
  小説の執筆、レビュー、修正適用などのすべての作業において、`data/sources/` 配下にある設定資料・プロット・キャラクター概要を最優先のソース（真実の基準）として参照してください。推測や独自の判断で世界観設定、歴史、キャラクターの口調・設定を捏造または逸脱させてはなりません。

## 5. レビュー結果の確認と適用（WebUI優先ルール）
- **WebUI優先での確認・適用**:
  ユーザーから「レビュー結果を反映して」「レビュー結果を見せて」「推敲内容を確認したい」などの指示を受けた場合は、チャット上で指摘リストを展開して対話的に適用するのではなく、WebUIである **「Novel Studio (WebUI)」** を通じてブラウザ上で確認・適用することを案内してください。
  WebUIサーバーがまだ起動していない場合は、`poetry run review-server` を実行して起動し、ユーザーにブラウザを開くよう促してください。
- **反映時のセーフガードとCUI適用**:
  指摘を小説テキストに反映する際は、ユーザーが `accepted: "y"` とマークした指摘のみを正確に反映し、`accepted: "n"` またはその他の項目は変更しないでください。
  また、チャット上でユーザーが直接反映を望む場合は、エージェントがテキストを手動で直接編集して置換することは避け、`poetry run apply-findings` スクリプトを使用して自動反映を行ってください。
- **レビューパイプライン実行とWebUI連携**:
  特定の小説のレビューを求められた場合は、`poetry run run-review novels/<filename>` を実行してください。このコマンドは、並列レビュー実行後に自動的にWebUIサーバーを起動し、ブラウザを開きます。完了後はWebUI上で確認と適用を行うようユーザーに案内してください。

## 6. WebUIの実装および修正方針
- **WebUI（Novel Studioなど）の開発・修正**:
  WebUIのフロントエンド・バックエンドの新規実装や機能修正を行う際は、専用の [WebUI-Developer スキル](../skills/webui-developer/SKILL.md) を参照し、その設計思想およびガイドライン（非同期処理制御、エラーハンドリング、永続化、リアルタイムログコンソール等）を厳格に遵守してください。
