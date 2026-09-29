import requests
import json
import csv
import os

def getDataFromApi(query: str, hitsPerPage: int = 20, timeout: int = 10):
    API = 'https://hn.algolia.com/api/v1/search'
    params = {
        'query': query,
        'tags': 'story',
        'hitsPerPage': hitsPerPage
    }
    headers = {"User-Agent": "AI-Data-Collector/1.0 (Research Project)"}

    try:
        response = requests.get(API, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.Timeout:
        print("[ERROR] The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("[ERROR] A connection error occurred. Check your URL or internet connection.")
    except requests.exceptions.HTTPError as err:
        print(f"[ERROR] HTTP error occurred: {err}")
    except requests.exceptions.JSONDecodeError:
        print("[ERROR] Failed to parse response as JSON.")
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] An unexpected network error occurred: {err}")
    return None

def extractData(rawData):
    extracted_data = []
    hits = rawData.get("hits", [])

    for item in hits:
        title = item.get("title") or ""
        if not title.strip():
            continue

        record = {
            "id": item.get("objectID", ""),
            "title": title.strip(),
            "author": item.get("author", "unknown"),
            "points": item.get("points") if item.get("points") is not None else 0,
            "num_comments": item.get("num_comments") if item.get("num_comments") is not None else 0,
            "created_at": item.get("created_at", ""),
            "url": item.get("url", "")
        }
        extracted_data.append(record)

    return extracted_data

def analyzeData(data):
    if not data:
        print("[INFO] No data available for analysis.")
        return

    total_points = sum(item["points"] for item in data)
    avg_points = total_points / len(data)

    highest_scoring = max(data, key=lambda x: x["points"])
    most_commented = max(data, key=lambda x: x["num_comments"])

    print("\n--- DATA ANALYSIS RESULTS ---")
    print(f"Total Records Analyzed: {len(data)}")
    print(f"Average Points per Story: {avg_points:.2f}")
    print(f"Highest Scoring Story: '{highest_scoring['title']}' ({highest_scoring['points']} points)")
    print(f"Most Commented Story: '{most_commented['title']}' ({most_commented['num_comments']} comments)")
    print("-----------------------------\n")

def save_json(data, filename='hn_ai_dataset.json'):
    try:
        with open(filename, mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"[SUCCESS] Data successfully saved to {filename}")
    except (IOError, OSError, PermissionError) as err:
        print(f"[ERROR] Failed to write JSON file '{filename}': {err}")

def save_csv(data, filename='hn_ai_dataset.csv'):
    if not data:
        print("[ERROR] No data provided to write to CSV.")
        return
    try:
        fieldnames = list(data[0].keys())
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"[SUCCESS] Data successfully saved to {filename}")
    except (IOError, OSError, PermissionError) as err:
        print(f"[ERROR] Failed to write CSV file '{filename}': {err}")

def verify_saved_files(json_filename='hn_ai_dataset.json', csv_filename='hn_ai_dataset.csv'):
    print("[INFO] Starting verification of stored data files...")
    
    try:
        print(f"Attempting to read '{json_filename}'...")
        with open(json_filename, mode='r', encoding='utf-8') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] JSON file '{json_filename}' was not found.")
    except json.JSONDecodeError as err:
        print(f"[ERROR] JSON file '{json_filename}' contains invalid JSON: {err}")
    except (IOError, OSError) as err:
        print(f"[ERROR] Failed to read JSON file '{json_filename}': {err}")
    else:
        print(f"[VERIFY SUCCESS] JSON file contains {len(json_data)} valid records.")
    finally:
        print("Completed JSON verification attempt.")

    try:
        print(f"Attempting to read '{csv_filename}'...")
        with open(csv_filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)
    except FileNotFoundError:
        print(f"[ERROR] CSV file '{csv_filename}' was not found.")
    except csv.Error as err:
        print(f"[ERROR] CSV file '{csv_filename}' formatting error: {err}")
    except (IOError, OSError) as err:
        print(f"[ERROR] Failed to read CSV file '{csv_filename}': {err}")
    else:
        print(f"[VERIFY SUCCESS] CSV file contains {len(csv_data)} rows.")
    finally:
        print("Completed CSV verification attempt.")

if __name__ == "__main__":
    query_input = input("Enter search query (e.g., Artificial Intelligence, LLM, OpenAI): ").strip()
    if not query_input:
        query_input = "Artificial Intelligence"
        print(f"[INFO] Empty input. Using default query: '{query_input}'")

    hits_input = input("Enter max hits to pull per page [default 20]: ").strip()
    if hits_input == "":
        hits_per_page = 20
    else:
        try:
            hits_per_page = int(hits_input)
            if hits_per_page <= 0:
                print("[WARNING] Hit count must be positive. Falling back to default (20).")
                hits_per_page = 20
        except ValueError:
            print("[WARNING] Invalid number entered. Falling back to default (20).")
            hits_per_page = 20

    print(f"\n[INFO] Fetching AI research data for query: '{query_input}' (Max hits: {hits_per_page})...")
    raw_response = getDataFromApi(query=query_input, hitsPerPage=hits_per_page)

    if raw_response:
        clean_records = extractData(raw_response)
        print(f"[INFO] Extracted {len(clean_records)} valid records.")

        if clean_records:
            analyzeData(clean_records)
            save_json(clean_records, filename='hn_ai_dataset.json')
            save_csv(clean_records, filename='hn_ai_dataset.csv')
            print("\n[INFO] Verifying saved local files...")
            verify_saved_files(json_filename='hn_ai_dataset.json', csv_filename='hn_ai_dataset.csv')
            print("\n[SUCCESS] AI experiment pipeline completed successfully!")
        else:
            print("[INFO] No matching records found.")
    else:
        print("[ERROR] Pipeline stopped due to network or connection failure.")