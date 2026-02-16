import sys
import re

def format_novel(text):
    """
    NotebookLMなどで執筆された小説をウェブ小説向けにフォーマットする。
    1. 句読点（。、）の後の不自然なスペースを削除。
    2. 文末の参照番号（数字）を削除。
    3. ウェブ小説向けの改行制度（文ごとの改行、段落間の空行、台詞の独立）を適用。
    """
    
    # 1. 句読点（。、）の後の不自然なスペースを削除
    text = re.sub(r'([。、])[\s　]+', r'\1', text)
    
    # 2. 文末の参照番号と思われる数字を削除
    text = re.sub(r'([。、！？」』])\d+(?=\s|$)', r'\1', text)
    
    # 3. ウェブ小説向けの改行調整
    # 文末（。！？）の後に改行がない場合、改行を挿入する
    text = re.sub(r'([。！？])(?![\n」』])', r'\1\n', text)
    
    # 台詞（「 『）の開始前で改行を入れる
    text = re.sub(r'(?<!\n)([「『])', r'\n\1', text)
    # 台詞の終了後で改行を入れる
    text = re.sub(r'([」』])(?!\n)', r'\1\n', text)
    
    lines = text.splitlines()
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        formatted_lines.append(line)
        # 基本的に全ての行の後に空行を入れる（ウェブ小説スタイル）
        formatted_lines.append("")
            
    # 連続する空行を整理（3つ以上の改行を2つに）
    result = "\n".join(formatted_lines).strip()
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                content = f.read()
            print(format_novel(content))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 標準入力から読み込み
        content = sys.stdin.read()
        if content:
            print(format_novel(content))

if __name__ == "__main__":
    main()
