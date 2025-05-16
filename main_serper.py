import pandas as pd
import requests
import re
import time

UNWANTED_LOCATIONS = {"india", "gujarat", "maharashtra", "delhi", "jammu", "bangalore", "mumbai", "ahmedabad"}
API_KEY = "your-serper-api-key"

def get_best_match(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}

    response = requests.post(url, json=data, headers=headers)
    results = response.json()

    if "organic" in results:
        for result in results["organic"][:3]:
            title = result.get("title", "").strip()
            if title and title.lower() not in UNWANTED_LOCATIONS:
                return title
    return "Not Found"

def main():
    df = pd.read_excel("data/companylist.xlsx")
    sample_df = df.head(2500)
    results = []

    for company in sample_df["company"]:
        cleaned_query = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", str(company), flags=re.IGNORECASE)
        cleaned_query = re.sub(r"\s+", " ", cleaned_query).strip()
        best_name = get_best_match(cleaned_query)

        if "..." in best_name:
            best_name = best_name.replace("...", "").strip()
            last_amp = best_name.rfind("&")
            if last_amp != -1:
                best_name = best_name[:last_amp] + best_name[last_amp+1:]
            if "," in best_name:
                parts = best_name.rsplit(",", 1)
                after_comma = parts[1].strip().lower()
                if len(after_comma.split()) <= 2 or after_comma in UNWANTED_LOCATIONS:
                    best_name = parts[0].strip()

        results.append({
            "Old Company Name": company,
            "New Company Name": best_name
        })

        print(f"Searching : {company} \n→ {best_name}")
        time.sleep(1.5)

    result_df = pd.DataFrame(results)
    result_df.to_excel("output/cleaned_companies.xlsx", index=False)
    print("Saved to output/cleaned_companies.xlsx")

if __name__ == "__main__":
    main()
