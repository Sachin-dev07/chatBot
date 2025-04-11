from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__, template_folder="templates", static_folder="static")

openai.api_key = "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"

mock_adventures = {
    "hiking": [
        {"name": "Triund Trek", "location": "Himachal Pradesh", "difficulty": "Easy-Moderate"},
        {"name": "Valley of Flowers", "location": "Uttarakhand", "difficulty": "Moderate"},
        {"name": "Kedarkantha Trek", "location": "Uttarakhand", "difficulty": "Moderate"},
        {"name": "Dzongri Trek", "location": "Sikkim", "difficulty": "Challenging"},
        {"name": "Chembra Peak", "location": "Kerala", "difficulty": "Easy"}
    ],
    "biking": [
        {"name": "Manali to Leh", "location": "Himachal to Ladakh", "difficulty": "Hard"},
        {"name": "Munnar to Thekkady", "location": "Kerala", "difficulty": "Moderate"},
        {"name": "Coorg Loop Ride", "location": "Karnataka", "difficulty": "Easy"},
        {"name": "Shillong to Cherrapunji", "location": "Meghalaya", "difficulty": "Moderate"},
        {"name": "Rann of Kutch Trail", "location": "Gujarat", "difficulty": "Easy"}
    ],
    "outdoor": [
        {"name": "Paragliding", "location": "Bir Billing, Himachal Pradesh", "type": "Adventure"},
        {"name": "River Rafting", "location": "Rishikesh, Uttarakhand", "type": "Water Sport"},
        {"name": "Scuba Diving", "location": "Havelock Island, Andaman", "type": "Water Sport"},
        {"name": "Hot Air Balloon", "location": "Jaipur, Rajasthan", "type": "Aerial"},
        {"name": "Caving", "location": "Meghalaya (Siju, Mawsmai)", "type": "Exploration"},
        {"name": "Wildlife Safari", "location": "Jim Corbett, Kaziranga, Ranthambore", "type": "Wildlife"}
    ]
}

def fetch_adventures(activity_type):
    return mock_adventures.get(activity_type.lower(), [])

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI outdoor adventure planner focused on Indian destinations."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").lower()

    if any(word in user_input for word in ["hike", "hiking", "trek"]):
        adventures = fetch_adventures("hiking")
    elif any(word in user_input for word in ["bike", "biking", "cycling"]):
        adventures = fetch_adventures("biking")
    elif any(word in user_input for word in ["paraglide", "rafting", "scuba", "caving", "safari", "outdoor"]):
        adventures = fetch_adventures("outdoor")
    else:
        return jsonify({"response": ask_openai(user_input)})

    # Format the response
    response_text = "Here are some great adventure spots in India:\n\n"
    for adv in adventures:
        if "difficulty" in adv:
            response_text += f"• {adv['name']} - {adv['location']} ({adv['difficulty']})\n"
        elif "type" in adv:
            response_text += f"• {adv['name']} in {adv['location']} [{adv['type']}]\n"
        else:
            response_text += f"• {adv['name']} - {adv['location']}\n"

    return jsonify({"response": response_text.strip()})

if __name__ == "__main__":
    app.run(debug=True)