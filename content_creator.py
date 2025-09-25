import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_email(lead_data, product_info):
    """
    Uses a generative AI model to create a personalized cold email.
    The prompt is crucial for the quality of the output.
    """
    company_name = lead_data["company_name"]
    contact_name = lead_data["contact_name"]
    contact_role = lead_data["contact_role"]

    prompt = (
        f"You are an expert sales representative. Your goal is to write a compelling cold email "
        f"to {contact_name}, the {contact_role} at {company_name}. "
        f"The email should be personalized and relevant to their role. "
        f"The product you are selling is {product_info['name']}. "
        f"It has the following benefits: {product_info['benefits']}. "
        f"The email should be concise, professional, and end with a call to action. "
        f"Do not use filler words or generic phrases. The tone should be helpful, not pushy."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Use a capable model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating email: {e}"

def run_content_creator():
    print("Content-Creator Agent is drafting emails...")
    
    # Load leads from the CSV file
    try:
        with open('data/leads.csv', 'r') as f:
            reader = csv.DictReader(f)
            leads = list(reader)
    except FileNotFoundError:
        print("Error: leads.csv not found. Please run the Information-Scout agent first.")
        return

    # Define your product
    my_product = {
        "name": "Auto-SDR AI Agent",
        "benefits": "Automates lead research, qualifies prospects, and writes personalized emails."
    }

    for lead in leads:
        email_content = generate_email(lead, my_product)
        print(f"\n--- Email for {lead['contact_name']} at {lead['company_name']} ---")
        print(email_content)
        print("-" * 50)
        
    print("\nContent-Creator Agent finished drafting all emails.")
