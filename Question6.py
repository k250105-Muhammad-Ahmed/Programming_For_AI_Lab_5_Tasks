import requests

API='http://localhost:3000/predictions'


def GET():
    try:
        response=requests.get(API)

        response.raise_for_status()

        data=response.json()

        if data:
            for i in range(len(data)):
                print(f"ID: {data[i].get('id')}")
                print(f"Image name: {data[i].get('image_name')}")
                print(f"Label: {data[i].get('label')}")
                print(f"Confidence: {data[i].get('confidence')}")
        else:
            print("No data was found")

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("A connection error occurred. Check your URL or internet connection.")
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse response as JSON. Ensure your API_URL is correct.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

def POST():
    new_prediction = {
        "image_name": "cat_test.jpg",
        "label": "cat",
        "confidence": 0.94
    }
    try:
        response=requests.post(API,json=new_prediction)

        response.raise_for_status()

        print(f"HTTP Status Code: {response.status_code}") 
        print("JSON Response Payload:")
        print(response.json())
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST operation: {e}")

def PUT():
    record_id = '3eHGMa8F4Xo'
    
    ITEM_API = f"http://localhost:3000/predictions/{record_id}"
    edit_prediction={
    "image_name": "cat_test.jpg",
    "label": "panther",
    "confidence": 0.99
    }
    try:
        response=requests.put(ITEM_API,json=edit_prediction)

        response.raise_for_status()

        print(f"HTTP Status Code: {response.status_code}") 
        print("JSON Response Payload:")
        print(response.json())
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST operation: {e}")

def DELETE():
    record_id = '3eHGMa8F4Xo'
        
    ITEM_API = f"http://localhost:3000/predictions/{record_id}"

    try:
        response=requests.delete(ITEM_API)

        response.raise_for_status()
        
        print(f"HTTP Status Code: {response.status_code}") 
        print("JSON Response Payload:")
        print(response.json())
                    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST operation: {e}")

if __name__=="__main__":
    POST()
    GET()
    PUT()
    DELETE()
