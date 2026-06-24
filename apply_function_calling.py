import re
import tool
from tool import analyze_symptoms, get_recommended_action
from safety import evaluate_patient_safety
import model_function_calling
from model_function_calling import build_llm_model, call_llama_with_chat_template
import json





tools = [
    {
        "type": "function",
        "function": {
            "name": "analyze_symptoms",
            "description": "Look up patient symptoms and return possible condition and follow-up question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The exact original patient symptom query."
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "get_recommended_action",
            "description": "based on the patient prompt, return the recommended action.",
            "parameters":{
                "type": "object",
                "properties":{
                    "prompt":{
                        "type": "string",
                        "description": "The exact original patient symptom query"
                        }
                },
                    "required": ["prompt"]
            }
        }
    }
]







def run_react_agent(patient_prompt: str):
    
    safety_alert = evaluate_patient_safety(patient_prompt)
    if safety_alert:
        return safety_alert

    messages = [
        {"role": "system",
         "content": (
            "You are a safe healthcare triage assistant."
            "You are Not a doctor. Use tools analyze_symptoms and get_recommended_action to give medical assistance including possible condition, follow-up question, recommended action.")},
        {"role": "user", "content": patient_prompt},
    ]

    tool_function = {
        "analyze_symptoms": analyze_symptoms,
        "get_recommended_action": get_recommended_action
    }

    
    model, tokenizer = build_llm_model()
    used_tools = set()
    total_tools = {"analyze_symptoms", "get_recommended_action"}

    for step in range(5):

        # extract the model output text
        model_output = call_llama_with_chat_template(model, tokenizer,messages, tools)
        match = re.search(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", model_output, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            json_text = model_output
        model_output = json.loads(json_text)

        # check if information from both tools obtained by model
        missing_tools = total_tools - used_tools
        
        if len(missing_tools) == 0:
            messages.append({
                "role": "user",
                "content": "Both tools are complete. Now give the final patient-facing answer based on  the information from the tools (include possible condition, follow-up question to ask, recommended action). Do not call any tools. Do not make up suggestions. Suggest visit doctor if needed."
            })
            return call_llama_with_chat_template(model, tokenizer, messages, tools = [])

        if model_output["name"] == "analyze_symptoms" or model_output["name"] == "get_recommended_action":
            tool_name = model_output["name"]
            tool_args = model_output["arguments"]

            if tool_name not in used_tools:
                used_tools.add(tool_name)
                observation = tool_function[tool_name](** tool_args)
                messages.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": observation
                    })
                print(observation)
            else:
                messages.append({
                    "role": "user",
                    "content":  f"You already called {tool_name}. Now call the missing tool from {missing_tools} only"
                })
            continue
        else:
            return model_output.final_text
    return "The agent took too many steps"



if __name__ == "__main__":
    result = run_react_agent("he sometimes fever feel headaches, but not frequently, not always")
    print(f"the agent response is: {result}")


































# format of the prompt needs to give as input to LLM everytime
# [System Prompt Rules Manual...]
# Patient Query: chest pain

# Thought: I need to check the baseline conditions for these symptoms.
# Action: analyze_symptoms
# Action Input: chest pain
# Observation: Matches dataset for 'chest pain'. Possible Conditions: heart attack risk. Suggested Follow-up Question to ask patient: 'Do you have shortness of breath?'

# Thought: I see the possible condition. Now I must find the recommended action.
# Action: get_recommended_action
# Action Input: chest pain
# Observation: Recommended Action for 'chest pain': seek emergency care.