
import re
import pandas as pd
from pathlib import Path


def parse_log_file(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    entries = []
    invalid_lines = []

    # Recognize timestamp, log level and message
    pattern = re.compile(
        r"^\s*(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
        r"\s+(?P<level>DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL)"
        r"\s+(?P<message>.*)$",
        re.IGNORECASE
    )

    with open(path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):

            raw_line = line.strip()

            if not raw_line:
                continue

            match = pattern.match(raw_line)

            if match:
                data = match.groupdict()

                level = data["level"].upper()

                if level == "WARN":
                    level = "WARNING"

                entries.append({
                    "line_number": line_number,
                    "timestamp": data["timestamp"],
                    "level": level,
                    "message": data["message"],
                    "raw_line": raw_line
                })

            else:
                invalid_lines.append({
                    "line_number": line_number,
                    "raw_line": raw_line,
                    "reason": "Log format not recognized"
                })

    # Convert parsed logs into DataFrames
    entries_df = pd.DataFrame(
        entries,
        columns=["line_number", "timestamp", "level", "message", "raw_line"]
    )

    invalid_df = pd.DataFrame(
        invalid_lines,
        columns=["line_number", "raw_line", "reason"]
    )

    levels = ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"]

    counts_df = (
        entries_df["level"].value_counts()
        .reindex(levels, fill_value=0)
        .rename_axis("level")
        .reset_index(name="count")
    )

    error_messages = entries_df[
        entries_df["level"].isin(["ERROR", "CRITICAL"])
    ][["line_number", "timestamp", "level", "message"]]

    return {
        "entries": entries_df,
        "counts": counts_df,
        "error_messages": error_messages,
        "invalid_lines": invalid_df
    }
