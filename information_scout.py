import requests
from bs4 import BeautifulSoup
import time
import csv

# Example function to get a list of companies from a search engine
def find_companies(query):
    """
    Simulates finding a list of companies based on a search query.
    In a real project, this would involve a search API or a more advanced web scraper.
    """
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # A simplified example of finding links; real scraping is more complex
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]
    
    companies = []
    # Filter for company websites based on a simple heuristic
    for link in links:
        if "linkedin.com" in link or "wikipedia.org" in link:
            continue
        # Basic parsing to get a company name from the URL
        company_name = link.split('//')[-1].split('/')[0].replace('www.', '').split('.')[0]
        if company_name and company_name not in [c['name'] for c in companies]:
            companies.append({"name": company_name, "website": link})
    
    return companies[:5] # Return top 5 for a simple demo

# Example function to get a contact person from a company website
def get_contact_info(website_url):
    """
    Simulates finding a contact person and their role from a company's website.
    This is highly simplified and would require more robust NLP in a real app.
    """
    try:
        response = requests.get(website_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # A very basic NLP-like check for common roles
        if "Head of Sales" in soup.text:
            return "Head of Sales", "John Doe"
        elif "VP of Marketing" in soup.text:
            return "VP of Marketing", "Jane Smith"
        else:
            return "Unknown", "Unknown"
    except Exception:
        return "Unknown", "Unknown"

# Main function of the agent
def run_information_scout(query):
    print(f"Information-Scout Agent is starting research for '{query}'...")
    companies = find_companies(query)
    leads = []
    for company in companies:
        role, contact = get_contact_info(company['website'])
        if contact != "Unknown":
            leads.append({
                "company_name": company['name'].title(),
                "contact_name": contact,
                "contact_role": role,
                "website": company['website']
            })
            print(f"  - Found lead: {contact} at {company['name'].title()}")
            time.sleep(1)  # Be a good internet citizen
            
    # Save the leads to a CSV file
    with open('data/leads.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["company_name", "contact_name", "contact_role", "website"])
        writer.writeheader()
        writer.writerows(leads)
        
    print("Information-Scout Agent finished. Leads saved to data/leads.csv")
    return leads
