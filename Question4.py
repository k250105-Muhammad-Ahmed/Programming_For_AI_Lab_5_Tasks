import requests
import json

def getDataFromAPI(name:str):
    API="https://api.genderize.io"

    params = {
        'name':name
    }

    try:
        response=requests.get(API,params=params,timeout=5)
        print(response.content)

        if response.status_code==200:
            data=response.json()

            input_name=data.get("name")
            confidence=data.get("probability")
            prediction=data.get("gender")

            if not prediction:
                print(f"The API responded, but the no data for {name}")
                return None

            print("\n--Machine Learning Data--")
            print(f"Name: {input_name}")
            print(f"Prediction: {prediction}")
            print(f"Confidence: {confidence*100}")

        else:
            print(f"Server responded with status code: {response.status_code}")

    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("A connection error occurred. Check your URL or internet connection.")
    except requests.exceptions.JSONDecodeError:
        print("Failed to parse response as JSON. Ensure your API_URL is correct.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

if __name__=="__main__":
    getDataFromAPI('Ali')