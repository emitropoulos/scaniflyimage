from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WORKDRIVE_FOLDER_ID = "jtwahed5153149d034cc6b6f22bdc2f0b786b"
ACCESS_TOKEN = os.environ.get("ZOHO_ACCESS_TOKEN")  # Set this in Render environment variables

@app.route("/upload", methods=["POST"])
def upload_file():
    file_url = request.form.get("url")
    if not file_url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        # Download the file from the presigned URL
        file_data = requests.get(file_url)
        file_data.raise_for_status()

        # Upload to Zoho WorkDrive
        response = requests.post(
            "https://upload.zoho.com/v1/upload",
            headers={
                "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
            },
            files={"content": ("image.jpg", file_data.content)},
            data={"folderId": WORKDRIVE_FOLDER_ID}
        )

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
