import json
import argparse
from collections import Counter
import pandas as pd
import os 

def classify_error(message):
    msg = message.lower()

    # Core error categories
    if "no such file or directory" in msg or "not found" in msg:
        return "Missing/Incorrect Libraries"
    elif "unsupported output format" in msg or "no code blocks found" in msg:
        return "Prompt Handling/Format Error"
    elif "interpreter" in msg and "tflite" in msg:
        return "Invalid TensorFlow Lite Usage"
    elif "tensorflow::" in msg and ("interpreter" in msg or "microtensorarena" in msg):
        return "Invalid Custom TensorFlow Usage"
    elif "does not name a type" in msg or "has no member named" in msg:
        if "tflite" in msg or "tensorflow" in msg:
            return "Invalid TensorFlow Lite Usage"
        else:
            return "Symbol/Class API Issues"
    elif "code generation process failed" in msg or "failed to generate valid code" in msg:
        return "Code Generation Failure"
    elif "undefined reference to `setup'" in msg or "undefined reference to `loop'" in msg:
        return "Missing Main Functions"
    elif "failed to parse application specifications" in msg or "failed to generate valid application specifications" in msg:
        return "Specification Parsing Failure"
    elif "serviceunavailableerror" in msg or "connection refused" in msg or "ollama error occurred" in msg or "api connection error" in msg:
        return "LLM Runtime/Backend Error"
    elif "generation failed" in msg or "sketch generation failed" in msg:
        return "Generation Process Failure"

    # Subtle and expanded error types
    elif "exception caught in prompting attempt" in msg:
        return "Prompt Execution Error"
    elif "stray" in msg or "conflicting declaration" in msg or "expected primary-expression" in msg or "expected unqualified-id" in msg:
        return "Syntax Error in Generated Code"
    elif "was not declared in this scope" in msg and (
        "tcs34725" in msg or "integrationtime" in msg or "hardware" in msg or "sensor" in msg
    ):
        return "Sensor/Hardware Constant Not Declared"
    elif "tensor_arena_size" in msg or "tensor_arena" in msg:
        return "Invalid TensorFlow Lite Usage"
    elif "in function `main'" in msg or "in function 'void setup()'" in msg or "in function 'int error_reporter_printf" in msg:
        return "Code Generation Failure"
    elif "in file included from" in msg:
        return "Include/Import Error"
    elif "loadbinaryfile" in msg and "not declared in this scope" in msg:
        return "Missing Utility Function"
    elif "'tflite' is not a namespace-name" in msg or "'tflite' has not been declared" in msg:
        return "Invalid TensorFlow Lite Usage"
    elif "'micromutableopresolver' in namespace 'tflite'" in msg:
        return "Invalid TensorFlow Lite Usage"

    # Ignore user actions
    elif "keyboard interrupt received" in msg:
        return "Do not Count"

    # Otherwise, unknown
    else:
        return "Uncategorized"

def main(input_path, csv_out, cleaned_json_out):
    # Load file
    with open(input_path, "r") as f:
        errors = json.load(f)

    # Filter out tracebacks
    filtered = [e for e in errors if e.get("timestamp", "").lower() != "unknown"]

    # Classify
    categories = [classify_error(e["message"]) for e in filtered]
    freq = Counter(categories)

    # Save CSV
    df = pd.DataFrame(freq.items(), columns=["Meta-Category", "Frequency"]).sort_values(by="Frequency", ascending=False)
    df.to_csv(csv_out, index=False)

    # Save cleaned JSON
    with open(cleaned_json_out, "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"✔ Done!\n→ Summary CSV: {csv_out}\n→ Cleaned JSON: {cleaned_json_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify error logs by category.")
    parser.add_argument("input", help="Path to input JSON file")
    #parser.add_argument("--csv", default="classified_error_summary.csv", help="Path to output CSV file")
    #parser.add_argument("--cleaned", default="cleaned_errors.json", help="Path to output cleaned JSON file")

    args = parser.parse_args()

    input_base = os.path.splitext(os.path.basename(args.input))[0]
    csv_out = f"{input_base}_summary.csv"
    cleaned_json_out = f"{input_base}_cleaned.json"


    #main(args.input, args.csv, args.cleaned)
    main(args.input, csv_out, cleaned_json_out)