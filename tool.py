#!/usr/bin/env python
# coding: utf-8

# Setup (run once if needed):
# pip uninstall kagglehub kagglesdk -y
# pip install "kagglehub==0.4.3" kagglesdk

# import kagglehub
# kagglehub.login()

import kagglehub
import pandas as pd
from pathlib import Path

COMPETITION = "healthcare-ai-agent-hackathon-build-real-world-agents"

path = kagglehub.competition_download(COMPETITION)
print("Path to competition files:", path)

healthcare_agent_data = pd.read_csv(
    Path(path) / "healthcare_ai_agent_dataset.csv"
)


def build_symptom_lookup(healthcare_agent_data: pd.DataFrame) -> dict:
    """Map each symptom string to follow-up, condition, and action info."""
    lookup = {}
    for _, row in healthcare_agent_data.iterrows():
        lookup[row["symptoms"]] = {
            "follow_up_question": row["follow_up_question"],
            "possible_condition": row["possible_conditions"],
            "recommended_action": row["recommended_action"],
        }
    return lookup


symptom_lookup = build_symptom_lookup(healthcare_agent_data)


def analyze_symptoms(prompt: str) -> None:
    """
    Match prompt against symptom_lookup keys and print guidance when found.

    Comma-separated key parts can appear in any order and need not be adjacent.
    """
    prompt_lower = prompt.lower()
    best_key = None
    best_info = None
    best_part_count = 0

    for symptom_key, info in symptom_lookup.items():
        parts = [part.strip().lower() for part in symptom_key.replace(",", " ").split() if part.strip()]
        if not parts:
            continue
        if all(part in prompt_lower for part in parts):
            if len(parts) > best_part_count:
                best_key = symptom_key
                best_info = info
                best_part_count = len(parts)

    if best_key is None:
        return(f"{prompt} not found in symptom lookup.")
        

    return(
        f"find the match with {best_key}, "
        f"the possible condition could be {best_info['possible_condition']}, "
        f"suggest the follow-up question to ask patient could be {best_info['follow_up_question']}"
    )


def get_recommended_action(prompt: str) -> None:
    """
    Match prompt against symptom_lookup keys and print recommended action when found.

    Comma-separated key parts can appear in any order and need not be adjacent.
    """
    prompt_lower = prompt.lower()
    best_key = None
    best_info = None
    best_part_count = 0

    for symptom_key, info in symptom_lookup.items():
        parts = [part.strip().lower() for part in symptom_key.replace(",", " ").split() if part.strip()]
        if not parts:
            continue
        if all(part in prompt_lower for part in parts):
            if len(parts) > best_part_count:
                best_key = symptom_key
                best_info = info
                best_part_count = len(parts)

    if best_key is None:
        return(f"{prompt} not found")


    return(f"recommend action could be {best_info['recommended_action']}")


if __name__ == "__main__":
    analyze_symptoms("cough, and sometimes cold")
    get_recommended_action("little cough, after get a little cold")
