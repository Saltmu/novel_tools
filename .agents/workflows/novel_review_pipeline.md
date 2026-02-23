---
description: Run the entire novel review pipeline (Formatting -> Parallel Review Skills) and save the results in `novel_check_results`.
---

# Novel Review Pipeline

This workflow executes all available skills, running independent reviews in parallel to speed up the process, and saves the output to a `novel_check_results` directory.

// turbo-all
1. Create the `novel_check_results` directory if it does not exist.
```bash
mkdir -p novel_check_results
```

2. Format the novel and save the output. Please replace `[TARGET_FILE]` with the path to the novel text file you want to review. Wait for this step to complete before proceeding, as other skills depend on the formatted text!
```bash
echo "Agent: Please run novel-formatter on [TARGET_FILE] and save to novel_check_results/01_formatted.txt. Wait for completion."
```

3. Once formatting is complete, run the following 7 review skills **in parallel** (issue tool calls concurrently or utilize parallel processing where possible) on the formatted text `novel_check_results/01_formatted.txt`. 

- `world-logic-guard` -> `novel_check_results/02_world_logic.md`
- `consistency-checker` -> `novel_check_results/03_consistency.md`
- `show-dont-tell-enhancer` -> `novel_check_results/04_show_dont_tell.md`
- `foreshadowing-tracker` -> `novel_check_results/05_foreshadowing.md`
- `plot-pacing-analyzer` -> `novel_check_results/06_pacing.md`
- `rhythm-vocabulary-optimizer` -> `novel_check_results/07_rhythm.md`
- `character-voice-checker` -> `novel_check_results/08_character_voice.md`

```bash
echo "Agent: Please execute the above 7 skills in parallel to generate the review reports."
```