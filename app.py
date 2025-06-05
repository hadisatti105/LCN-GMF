from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

PING_URL = "https://growmyfirmonline.leadspediatrack.com/ping.do"
POST_URL = "https://growmyfirmonline.leadspediatrack.com/post.do"

LP_CAMPAIGN_ID = "683f5e68876ab"
LP_CAMPAIGN_KEY = "gj8bMhJXkRG7DqdW4nw2"

@app.route('/', methods=['GET', 'POST'])
def index():
    response_message = None

    if request.method == 'POST':
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        # 1. PING Request
        ping_payload = {
            "lp_campaign_id": LP_CAMPAIGN_ID,
            "lp_campaign_key": LP_CAMPAIGN_KEY,
            "lp_response": "json",

            "zip_code": request.form.get("zip_code"),
            "incident_date": request.form.get("incident_date"),
            "doctor_treatment": request.form.get("doctor_treatment"),
            "were_you_at_fault": request.form.get("were_you_at_fault"),
            "currently_represented": request.form.get("currently_represented"),
            "mva_accident_type": request.form.get("mva_accident_type")
        }

        ping_response = requests.post(PING_URL, data=ping_payload)
        ping_data = ping_response.json()

        if ping_data.get("result") != "success":
            response_message = json.dumps(ping_data, indent=2)
            return render_template('index.html', response_message=response_message)

        # 2. POST Request
        post_payload = {
            "lp_campaign_id": LP_CAMPAIGN_ID,
            "lp_campaign_key": LP_CAMPAIGN_KEY,
            "lp_ping_id": ping_data["ping_id"],
            "lp_response": "json",

            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email_address": request.form.get("email"),
            "phone_home": request.form.get("phone"),
            "zip_code": request.form.get("zip_code"),
            "incident_date": request.form.get("incident_date"),
            "doctor_treatment": request.form.get("doctor_treatment"),
            "were_you_at_fault": request.form.get("were_you_at_fault"),
            "currently_represented": request.form.get("currently_represented"),
            "mva_accident_type": request.form.get("mva_accident_type"),
            "primary_injury": request.form.get("primary_injury"),
            "general_description": request.form.get("description"),
            "landing_page_url": request.form.get("landing_page_url"),
            "tcpa_language": request.form.get("tcpa_language"),
            "lp_s1": request.form.get("lp_s1"),
            "trusted_form_cert_id": request.form.get("trusted_form"),
            "ip_address": ip_address,
            "user_agent": user_agent
        }

        post_response = requests.post(POST_URL, data=post_payload)
        post_data = post_response.json()
        response_message = json.dumps(post_data, indent=2)

    return render_template('index.html', response_message=response_message)

if __name__ == '__main__':
    app.run(debug=True)
