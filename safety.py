import re

# A compiled list of critical symptoms that require immediate human medical care
EMERGENCY_KEYWORDS = [
    r"chest\s*pain", 
    r"breathing\s*difficulty", 
    r"shortness\s*of\s*breath",
    r"severe\s*bleeding",
    r"stroke",
    r"numbness"
]

def evaluate_patient_safety(patient_query: str) -> str or None:
    """
    Scans the patient query using regex.
    Returns an emergency string if a red flag is found, otherwise returns None.
    """
    clean_query = patient_query.lower().strip()
    
    # Scan for any matches in our emergency keyword list
    for pattern in EMERGENCY_KEYWORDS:
        if re.search(pattern, clean_query):
            # If found, return the mandatory, non-negotiable safety warning
            return (
                "🚨 EMERGENCY WARNING: Your description contains signs of a potentially "
                "critical medical condition. I am an AI assistant, not a doctor. "
                "Please immediately call 911, visit the nearest emergency room, "
                "or seek immediate assistance from a qualified healthcare professional."
            )
            
    # Return None if the query is clear of immediate high-risk red flags
    return None