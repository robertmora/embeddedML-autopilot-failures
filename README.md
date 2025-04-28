# embeddedML-autopilot-failures

## Overview

Large Language Models (LLMs) are increasingly used to automate various stages of embedded machine learning (ML) workflows. However, they often introduce silent or difficult-to-detect failures.

This repository hosts:

- **Raw logs** collected from the **Embedded ML Autopilot** system, covering LLM interactions, responses, and downstream pipeline behavior.
- **Scripts** to:
  - **Jsonize** the raw logs into structured format.
  - **Classify** observed errors into categories.
- **Parsed outputs** (JSON) ready for further analysis.

These resources allow **reproduction** of the analysis and **extension** of failure characterization across different LLM models or system configurations.

The **Embedded ML Autopilot** system is introduced in the following paper:

> **Consolidating TinyML Lifecycle with Large Language Models: Reality, Illusion, or Opportunity?**  
> To appear in IEEE IoT Magazine. Preprint available in [arXiv](https://arxiv.org/pdf/2501.12420)

---

## Repository Structure

```
embeddedML-autopilot-failures/
├── data/
│   ├── raw_logs/        # Raw log files collected during Autopilot experiments
│   └── parsed_logs/     # JSON-structured logs for analysis
├── scripts/
│   ├── jsonize_logs.py  # Script to parse raw logs into structured JSON
│   └── classify_errors.py # Script to classify parsed logs into error categories (taxonomy)
├── README.md
├── LICENSE
```

---

## What the Logs Contain

The logs in `data/raw_logs/` represent:

- **Sketch generation attempts** performed by the Embedded ML Autopilot system, where LLMs were tasked with producing Arduino-compatible C++ code (`.ino`) based on input data and hardware specifications.
- **Errors encountered** during different sketch generation stages, including:
  - Failures in parsing and filling application specifications.
  - LLM response parsing issues (e.g., missing or malformed JSON structures).
  - Compilation errors from generated code (e.g., missing headers, wrong API usage, missing symbols).
  - Communication errors with the LLM backend (e.g., Ollama server crashes).
- **LLM responses** and assumptions about the hardware, software libraries, and model tensor structures (e.g., input/output tensor dimensions).
- **Multiple retries** and dynamic handling strategies to recover from failures (e.g., re-prompting the LLM, retrying compilation).

Each log is linked to a **single sketch generation session**, covering the entire flow from user input acquisition to final compilation result or failure.

---

## Models Used

The sketch generation logs were generated using the following LLMs:

- **Codestral**
- **Gemma-3B**
- **GPT-4o**
- **Qwen 2.5 Coder**

Different models may show varying failure modes and robustness when tasked with the same sketch generation operations.

---

## How to Use

1. **Parse Raw Logs**

Converts raw `.log` logs into structured `.json` files:

```bash
python scripts/jsonize_logs.py
```

- Reads from: `data/raw_logs/`
- Writes to: `data/parsed_logs/`

2. **Classify Errors**

Assigns error categories:

```bash
python scripts/classify_errors.py
```

- Inputs: parsed JSON files in `data/parsed_logs/`
- Outputs: classified results (format depends on the script's logic)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
