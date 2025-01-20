from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization", "phNo", "accId"])


@app.route('/')
def hello_world():
    return 'Hello from Koyeb'
    

# First API: /process-api
@app.route('/process-api', methods=['POST'])
def process_api():
    # Get headers from the incoming request
    ph_no = request.headers.get('phNo')
    token = request.headers.get('Authorization')
    acc_id = request.headers.get('accId')

    # Check if required headers are present
    if not ph_no or not token or not acc_id:
        return jsonify({"error": "Missing required headers"}), 400

    # Format the API URL
    url = f"https://apis.mytel.com.mm/daily-quest-v3/api/v3/daily-quest/main-screen?clientType=Android&Platform=myid&msisdn=%2B95{ph_no}&revision=16226"

    # Make the external API call
    headers = {
        "Authorization": token
    }

    response = requests.get(url, headers=headers)

    # Handle errors from the external API
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from external API"}), response.status_code

    # Parse the JSON response
    data = response.json()

    # Modify the response if 'hl2package' exists
    hl2_package = data.get("result", {}).get("mainScreenResponse", {}).get("hl2package", {})
    if hl2_package.get("isComplete", False):
        return jsonify({"hl2Status": "available"})

    # Return the original API response if no modifications are needed
    return jsonify(data)
    
    


# Second API: /new-api
@app.route('/new-api', methods=['POST'])
def new_api():
    # Get headers from the incoming request
    ph_no = request.headers.get('phNo')
    token = request.headers.get('Authorization')
    acc_id = request.headers.get('accId')

    # Check if required headers are present
    if not ph_no or not token or not acc_id:
        return jsonify({"error": "Missing required headers"}), 400

    # Format the API URL
    url = f"https://apis.mytel.com.mm/daily-quest-v3/api/v3/daily-quest/main-screen?clientType=Android&Platform=myid&msisdn=%2B95{ph_no}&revision=16226"

    # Make the external API call
    headers = {
        "Authorization": token
    }

    response = requests.get(url, headers=headers)

    # Handle errors from the external API
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from external API"}), response.status_code

    # Parse the JSON response
    data = response.json()

    # Extract and process data from the main response
    main_screen = data.get("result", {}).get("mainScreenResponse", {})

    # Create the modified response
    custom_response = {
        "configCode": main_screen.get("miniQuest", [])[0].get("configCode", "ADD_NUMBER"),
        "title": main_screen.get("miniQuest", [])[0].get("title", "Link one new number"),
        "numCompleteAction": main_screen.get("miniQuest", [])[0].get("numCompleteAction", 0),
        "urlCallBack": main_screen.get("miniQuest", [])[1].get("urlCallBack", ""),
        "totalPrize": main_screen.get("totalPrize", 0),
        "background": main_screen.get("background", ""),
        "hl2Status": main_screen.get("hl2package", {}).get("isComplete", False)
    }

    # Return the custom response
    return jsonify(custom_response)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4050)
    