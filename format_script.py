import os
import re

input_file = '/home/sshioyama/ドキュメント/Antigravity/novel_tools/data/sources/01_重天の調律師_設定資料集.txt'
output_file = '/home/sshioyama/ドキュメント/Antigravity/novel_tools/data/sources/01_重天の調律師_設定資料集.md'

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []

for original in lines:
    line = original.lstrip()
    
    if not line.strip():
        output_lines.append("")
        continue
        
    line = line.rstrip()
    
    # Dividers
    if re.match(r'^_+', line) and len(line) > 5:
        output_lines.append("\n---\n")
        continue
        
    # Math
    if line.startswith('$$') and line.endswith('$$'):
        output_lines.append(f"\n$$\n{line[2:-2].strip()}\n$$\n")
        continue

    # Bullet lists
    if line.startswith('* '):
        output_lines.append("- " + line[2:])
        continue
    if line.startswith('• '):
        output_lines.append("- " + line[2:])
        continue
        
    # Headings detection
    is_list_item = bool(re.match(r'^(\-|\*|\•|\d+\.)', line))
    ends_with_punctuation = line.endswith(('。', '、', '」', '）', '.', ':', '：', '？', '！', '?', '!'))
    
    # Sections with ■
    if line.startswith('■'):
        output_lines.append(f"\n## {line.strip('■ ')}\n")
        continue

    # Numbered sections like '1. マクロな物理構造：『白亜の昇天樹』'
    if re.match(r'^\d+\.', line) and not ends_with_punctuation and len(line) < 50:
        if "：" in line or ":" in line or len(line) < 20: 
            output_lines.append(f"\n### {line}\n")
        else:
            output_lines.append(f"\n### {line}\n")
        continue
        
    # General title heuristic (short line, no punctuation at end, not a list item)
    if not is_list_item and not ends_with_punctuation:
        if len(line) < 20:
            output_lines.append(f"\n## {line}\n")
            continue
        elif len(line) < 40 and "：" in line:
            output_lines.append(f"\n### {line}\n")
            continue

    output_lines.append(line)

text = '\n'.join(output_lines)
# Clean up multiple empty lines
text = re.sub(r'\n{3,}', '\n\n', text)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(text.strip() + '\n')

print(f"Output written to {output_file}")
