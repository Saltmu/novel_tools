---
description: Run the entire novel review pipeline (Formatting -> Parallel Review Skills) in parallel across multiple files and save the results in `novel_check_results`.
---

# Novel Review Pipeline

This workflow executes all available skills for one or more novel files. It is designed to be highly parallel: multiple files can be processed independently, and for each file, multiple review skills are executed concurrently.

// turbo-all

0. Identify all target novel files (e.g., all `.txt` files in the `novels/` directory). **Steps 1-3 should be executed for each file independently and in parallel.**

1. Create a subdirectory for the results within `novel_check_results` named after the target file (e.g., `novel_check_results/[TARGET_FILE_BASENAME]`).
```bash
mkdir -p novel_check_results/[TARGET_FILE_BASENAME]
```

2. Format the novel and save the output. Please replace `[TARGET_FILE]` with the path to the novel text file you want to review. **Important:** Wait for this step to complete for the *specific file* before proceeding to Step 3 for that same file, as the review skills depend on its formatted text.
```bash
echo "Agent: Please run novel-formatter on [TARGET_FILE] and save to novel_check_results/[TARGET_FILE_BASENAME]/01_formatted.txt. Wait for completion of this file's formatting."
```

3. Once a file's formatting is complete, run the following 7 review skills **in parallel** on its formatted text `novel_check_results/[TARGET_FILE_BASENAME]/01_formatted.txt`. 

- `world-logic-guard` -> `novel_check_results/[TARGET_FILE_BASENAME]/02_world_logic.md`
- `consistency-checker` -> `novel_check_results/[TARGET_FILE_BASENAME]/03_consistency.md`
- `show-dont-tell-enhancer` -> `novel_check_results/[TARGET_FILE_BASENAME]/04_show_dont_tell.md`
- `foreshadowing-tracker` -> `novel_check_results/[TARGET_FILE_BASENAME]/05_foreshadowing.md`
- `plot-pacing-analyzer` -> `novel_check_results/[TARGET_FILE_BASENAME]/06_pacing.md`
- `rhythm-vocabulary-optimizer` -> `novel_check_results/[TARGET_FILE_BASENAME]/07_rhythm.md`
- `character-voice-checker` -> `novel_check_results/[TARGET_FILE_BASENAME]/08_character_voice.md`

```bash
echo "Agent: Please execute the above 7 skills in parallel to generate the review reports for [TARGET_FILE_BASENAME]."
```