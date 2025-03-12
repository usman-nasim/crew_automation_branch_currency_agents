#!/usr/bin/env python
import chainlit as cl
import pandas as pd
from crew_automation_branch_currency_agents.crew import CrewAutomationBranchCurrencyAgentsCrew

@cl.on_chat_start
async def start():
    # Prompt user to upload an Excel file
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload an Excel file to process branch currency data.",
            accept=["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],  # .xlsx files
            max_size=10  # Max 10MB
        ).send()
    
    excel_file = files[0]
    await cl.Message(content=f"File `{excel_file.name}` uploaded successfully! Processing...").send()

    # Define input paths
    inputs = {
        'knowledge_file_path': 'knowledge.xlsx',  # Assume a fixed knowledge file; adjust as needed
        'excel_file_path': excel_file.path,       # Path to the uploaded file
        'final_excel_file_path': 'final_output.xlsx',  # Intermediate Excel output
        'branch_name_mapping': 'dimension_codes',  # Placeholder; adjust if specific mapping is needed
        'intermediate_file_path': 'intermediate_output.xlsx'  # Intermediate file
    }

    # Run the crew
    crew = CrewAutomationBranchCurrencyAgentsCrew().crew()
    result = crew.kickoff(inputs=inputs)

    # Convert final Excel output to CSV
    final_excel_path = inputs['final_excel_file_path']
    df = pd.read_excel(final_excel_path)
    csv_path = 'final_output.csv'
    df.to_csv(csv_path, index=False)

    # Provide the CSV file for download
    await cl.Message(
        content="Processing complete! Download your filtered currency data below.",
        elements=[cl.File(name="final_output.csv", path=csv_path)]
    ).send()

if __name__ == "__main__":
    # Chainlit runs this automatically when you execute `chainlit run main.py`
    pass