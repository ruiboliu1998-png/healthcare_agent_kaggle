# healthcare_agent_kaggle
this is the solution for Kaggle hackathon healthcare agent AI
# Healthcare AI Agent
A Healthcare AI Agent built for the Kaggle Healthcare AI Agent Hackathon. The agent uses a ReAct-style reasoning workflow with tool calling to understand patient symptom queries, retrieve dataset-backed information, ask relevant follow-up questions, and suggest safe next steps.
> This project is for educational and hackathon purposes only. It does not provide medical diagnosis.
## Project Overview
AI agents can support healthcare workflows by helping patients describe symptoms, asking useful follow-up questions, and suggesting appropriate next steps. This project demonstrates a healthcare triage assistant that combines:
- Local LLM reasoning
- Dataset-backed symptom lookup
- Tool/function calling
- Safety screening for emergency symptoms
- Structured patient-facing responses
The agent does not replace a doctor. It provides possible conditions and recommended actions based on available dataset information.
## Key Features
- Understands patient symptom queries in natural language
- Uses a reasoning-action loop inspired by ReAct
- Calls external tools to retrieve possible conditions and recommended actions
- Asks relevant follow-up questions
- Includes basic safety guardrails for emergency symptoms
- Produces patient-friendly healthcare guidance
- Runs with open-source language models
## Agent Workflow
The agent follows this process:
1. Receive a patient symptom query.
2. Run a safety check for emergency warning signs.
3. Ask the LLM to select the next tool call.
4. Use `analyze_symptoms` to retrieve possible conditions and follow-up questions.
5. Use `get_recommended_action` to retrieve the suggested next step.
6. Generate a final structured response for the patient.
Example workflow:
```text
Patient Query:
"I have fever and headache sometimes"
Thought:
The agent needs to check symptoms against the healthcare dataset.
Action:
analyze_symptoms
Observation:
Possible condition and follow-up question are retrieved.
Action:
get_recommended_action
Observation:
Recommended action is retrieved.
Final Answer:
The agent provides a safe, structured patient-facing response.
```
## Project Structure
```text
healthcare_ai_agent/
├── apply_text_react.py
├── apply_function_calling.py
├── model.py
├── prompt.py
├── safety.py
├── tool.py
├── function_calling/
│   ├── apply_function_calling.py
│   ├── model_function_calling.py
│   ├── safety.py
│   └── tool.py
├── test_llm_mode.ipynb
└── improvement.txt
```
## Main Files
### `apply_text_react.py`
Implements the text-based ReAct loop using:
- `Thought`
- `Action`
- `Action Input`
- `Observation`
- `Final Answer`
### `function_calling/apply_function_calling.py`
Implements a function-calling style agent loop using structured tool calls.
### `tool.py`
Loads the healthcare dataset and provides two main tools:
- `analyze_symptoms`
- `get_recommended_action`
### `safety.py`
Checks patient queries for emergency red flags before the LLM generates a response.
### `model.py`
Loads the local LLM using Hugging Face Transformers.
### `prompt.py`
Defines the ReAct system prompt and tool-use rules.
## Tools
### `analyze_symptoms`
Looks up patient symptoms in the healthcare dataset and returns:
- Possible condition
- Suggested follow-up question
Example:
```python
analyze_symptoms("fever and headache")
```
### `get_recommended_action`
Looks up the recommended next step for the patient symptoms.
Example:
```python
get_recommended_action("fever and headache")
```
## Safety Design
The agent includes a safety check before running the reasoning loop. If the patient query contains emergency warning signs, the agent immediately returns an emergency warning instead of continuing with normal symptom analysis.
Current emergency examples include:
- Chest pain
- Breathing difficulty
- Shortness of breath
- Severe bleeding
- Stroke-related symptoms
- Numbness
Example emergency response:
```text
EMERGENCY WARNING:
Your description contains signs of a potentially critical medical condition.
I am an AI assistant, not a doctor. Please immediately call emergency services,
visit the nearest emergency room, or seek immediate assistance from a qualified
healthcare professional.
```
## Model
The project uses open-source instruction models through Hugging Face Transformers.
Current models used in the project include:
```text
meta-llama/Llama-3.2-3B-Instruct
Qwen/Qwen2.5-3B-Instruct
```
The models are loaded with 4-bit quantization using `bitsandbytes` to reduce memory usage.
## Requirements
Install the required dependencies:
```bash
pip install pandas kagglehub torch transformers bitsandbytes
```
Depending on your environment, you may also need:
```bash
pip install accelerate
```
## Dataset
The project uses the Kaggle competition dataset:
```text
healthcare_ai_agent_dataset.csv
```
The dataset is used to map symptoms to:
- Possible conditions
- Follow-up questions
- Recommended actions
The code currently uses `kagglehub` to download the competition dataset.
## How To Run
Run the ReAct version:
```bash
python apply_text_react.py
```
Run the function-calling version:
```bash
python function_calling/apply_function_calling.py
```
Example query inside the code:
```python
result = run_react_agent(
    "he sometimes fever feel headaches, but not frequently, not always"
)
print(result)
```
## Example Output
```text
Safety note: I am not a doctor, and this is not a medical diagnosis.
Possible condition:
The symptoms may be related to a mild infection or another condition listed in the dataset.
Follow-up question:
Do you have any other symptoms such as cough, sore throat, or body aches?
Recommended next step:
Monitor symptoms, rest, stay hydrated, and consult a healthcare professional if symptoms continue or worsen.
```
## Kaggle Submission
This project is designed for the Healthcare AI Agent hackathon.
A valid submission should include:
- Public Kaggle Notebook with full runnable code
- Kaggle Writeup explaining the project
- Demo video under 5 minutes
- Public GitHub repository
- Clear setup and run instructions
## Limitations
This is a prototype and has several limitations:
- Symptom matching is currently keyword-based.
- The safety red-flag list is basic and should be expanded.
- The function-call parser expects structured model output.
- The agent does not perform clinical diagnosis.
- The output quality depends on the local LLM response.
- Dataset coverage may be limited.
## Future Improvements
Planned improvements include:
- Add fuzzy matching for symptoms
- Add embedding-based retrieval
- Improve JSON/function-call parsing
- Expand emergency safety rules
- Add more test cases
- Add a simple user interface
- Improve final answer formatting
- Add notebook examples for Kaggle
- Add evaluation examples for common patient scenarios
## Medical Disclaimer
This project is not a medical device and is not intended to diagnose, treat, cure, or prevent disease.
The agent provides educational and informational support only. Users should always consult a qualified healthcare professional for medical advice. In an emergency, users should immediately contact local emergency services.
## License
This project is provided for educational and hackathon use.
