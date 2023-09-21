import requests
import json

class Functions_call:

    @staticmethod
    def send_email(to_email, subject, content):
        #API URL
        url = "https://gray-repulsive-duck.cyclic.app/sendEmail"

        # Headers
        headers = {
            "Content-Type": "application/json",
        }

        # the request body with the provided values
        payload = {
            "to": to_email,
            "subject": subject,
            "content": content,
        }

        # Convert the payload to JSON
        json_payload = json.dumps(payload)

        # Send the POST request
        response = requests.post(url, headers=headers, data=json_payload)

        # Check the response status code
        if response.status_code == 200:
            return "Email sent successfully!"
        else:
            return f"Failed to send email. Status code: {response.status_code}"

    # Weather function
    @staticmethod
    def get_current_weather(location):
        """Get the current weather in a given location"""

        url = f"https://open-weather13.p.rapidapi.com/city/{location}"

        headers = {
            "X-RapidAPI-Key": "27678da727mshb69f3fc5c4e5cf0p175e22jsnb10038e8caa6",
            "X-RapidAPI-Host": "open-weather13.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers)

        weather_info = response.json()

        print(weather_info)
        return json.dumps(weather_info)