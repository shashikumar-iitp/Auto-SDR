import os
import csv
from dotenv import load_dotenv

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Import the agents
from information_scout import run_information_scout
from content_creator import run_content_creator

def main():
    print("Starting the Auto-SDR Automation Workflow...")

    # Step 1: User input (simulated)
    target_profile = "new technology companies in India"
    
    # Step 2: Run the Information-Scout Agent
    leads = run_information_scout(target_profile)
    
    # Check if leads were found before proceeding
    if leads:
        # Step 3: Run the Content-Creator Agent
        run_content_creator()
    else:
        print("No leads were found. Ending the workflow.")

if __name__ == "__main__":
    main()
