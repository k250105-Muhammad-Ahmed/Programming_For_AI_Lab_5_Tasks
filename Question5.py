import requests
import json 
import csv
import os

def getDataFromApi(query:str,hitsPerPage:int=20,timeout:int=10):
    API='https://hn.algolia.com/api/v1/search'

    params={
        'query':query,
        'tags':'comment',
        'hitsPerPage':hitsPerPage
    }

    headers={"User-Agent": "NLP-Data-Collector/1.0 (Research Project)"}

    try:
        response=requests.get(API,params=params,headers=headers,timeout=timeout)

        response.raise_for_status()

        data=response.json()

        return data

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("A connection error occurred. Check your URL or internet connection.")
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse response as JSON. Ensure your API_URL is correct.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

    return None

def extractData(rawData):
    extracted_data=[]

    hits=rawData.get("hits",[])

    for item in hits: 
        text_content = item.get("comment_text") or item.get("title") or ""

        if not text_content.strip():
            continue

        record = {
            "id": item.get("objectID", ""),
            "text": text_content.strip(),
            "author": item.get("author", "unknown"),
            "created_at": item.get("created_at", ""),
            "points": item.get("points", 0),
            "story_title": item.get("story_title", ""),
            "story_url": item.get("story_url", ""),
        }

        extracted_data.append(record)

    return extracted_data

def save_json(data,filename='dataset.json'):
    try:
        with open(filename,mode='w',encoding='utf-8') as f:
            json.dump(data,f,indent=4)
        print(f"Data added to {filename}.json")
    except (IOError, OSError, PermissionError) as err:
        print(f"[ERROR] Failed to write JSON file '{filename}': {err}")

def save_csv(data,filename='dataset.csv'):

    if not data:
        print("No data")
        return
    try:
        fieldnames = list(data[0].keys())
        with open(filename,mode='w',encoding='utf-8',newline='') as f:
            fwriter=csv.DictWriter(f,fieldnames=fieldnames)
            fwriter.writeheader()
            fwriter.writerows(data)
        print(f"Data added to {filename}.csv")
    except (IOError, OSError, PermissionError) as err:
        print(f"[ERROR] Failed to write csv file '{filename}': {err}")

if __name__=="__main__":
    query_input = input("Enter search query (e.g., Python, AI): ").strip()
    
    if not query_input:
        print("[ERROR] Search query cannot be empty.")
        exit()

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

    print(f"\n[INFO] Fetching data for query: '{query_input}' (Max hits: {hits_per_page})...")
    
    raw_response = getDataFromApi(query=query_input, hitsPerPage=hits_per_page)
    
    if raw_response:
        clean_records = extractData(raw_response)
        print(f"[INFO] Extracted {len(clean_records)} valid records.")
        
        if clean_records:
            save_json(clean_records, filename='hn_dataset.json')
            save_csv(clean_records, filename='hn_dataset.csv')
            print("[SUCCESS] Pipeline completed successfully!")
        else:
            print("[INFO] No text blocks or titles discovered matching requirements.")
    else:
        print("[ERROR] Pipeline stopped due to network or connection failure.")