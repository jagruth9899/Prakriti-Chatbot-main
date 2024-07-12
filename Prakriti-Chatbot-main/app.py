import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize counters for Prakruti types
vata_count = 0
pitta_count = 0
kapha_count = 0

# Define the questions and regex patterns for responses
questions = [
    "What is the type of your body frame (Thin, Medium, Broad)?",
    "What is your Body Weight (Low, Moderate, Overweight)",
    "What is your skin type (Dry, Soft, Thick)?",
    "What is your hair type (Dry, Soft, Break)?",
    "What is your teeth type (Protruded, Moderate, Strong)?",
    "How are your eyes (Small, Sharp, Big)?",
    "How are your nails (Brittle, Soft, Thick)?",
    "How is your tongue (Cracked, Red, White Coated)?",
    "How is your pulse (Feeble, Moderate, Slow)?",
    "How is your emotional temperament (Moody, Aggressive, Calm)?",
    "How is your memory (Quick grasping, Moderate Grasping, Slow Grasping)?",
    "How is your initiation capabilities (Quick, Moderate, Slow)?",
    "How often do you communicate (Talkative, Moderate, Less)?",
    "Tolerance for seasonal weather (Cold intolerant, Heat intolerant, Tolerant to both)?",
    "How often do you perform physical activities (Very Active, Moderate, Lethargic)?",
]

response_patterns = [
    [(r'thin', 'vata'), (r'medium', 'pitta'), (r'broad', 'kapha')],
    [(r'low', 'vata'), (r'moderate', 'pitta'), (r'overweight', 'kapha')],
    [(r'dry|rough|cracked', 'vata'), (r'soft|thin|acnes|freckles', 'pitta'), (r'thick|oily|cool|clear complexion', 'kapha')],
    [(r'dry|thin|break', 'vata'), (r'soft|earlygreying', 'pitta'), (r'thick|oily', 'kapha')],
    [(r'protruded|big|gums emaciated|cavities', 'vata'), (r'moderate in size|yellowish|soft gums', 'pitta'), (r'strong|white', 'kapha')],
    [(r'small|dull|dry', 'vata'), (r'sharp|shiny', 'pitta'), (r'big|attractive|thick eye lashes', 'kapha')],
    [(r'brittle|dry|cracked', 'vata'), (r'soft|pink', 'pitta'), (r'thick|strong|shiny', 'kapha')],
    [(r'cracked', 'vata'), (r'red', 'pitta'), (r'white coated', 'kapha')],
    [(r'thready|feeble|moves like a snake', 'vata'), (r'moderate|jumping like a frog', 'pitta'), (r'slow|moves like a swan', 'kapha')],
    [(r'fearful|moody|unpredictable', 'vata'), (r'aggressive|jealous|impatience', 'pitta'), (r'calm|attached|likeable', 'kapha')],
    [(r'quick grasping | poor retention', 'vata'), (r'moderate grasping and retention', 'pitta'), (r'slow grasping | good retention', 'kapha')],
    [(r'quick|responsive', 'vata'), (r'moderate|understanding', 'pitta'), (r'slow', 'kapha')],
    [(r'talkative', 'vata'), (r'sharp| incisive communication with analytical abilities', 'pitta'), (r'less|less vocal| with good communication skill', 'kapha')],
    [(r'cold intolerant', 'vata'), (r'heat intolerant', 'pitta'), (r'tolerant to both heat and cold|both', 'kapha')],
    [(r'very active|active', 'vata'), (r'moderate', 'pitta'), (r'lethargic', 'kapha')],
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_prakruti', methods=['POST'])
def predict_prakruti():
    responses = request.json
    vata_count = 0
    pitta_count = 0
    kapha_count = 0

    # Process each response and accumulate counts
    for i, response in enumerate(responses):
        # Check the response against patterns for the current question
        for pattern, prakruti_type in response_patterns[i]:
            if re.search(pattern, response, re.IGNORECASE):
                if prakruti_type == 'vata':
                    vata_count += 1
                elif prakruti_type == 'pitta':
                    pitta_count += 1
                elif prakruti_type == 'kapha':
                    kapha_count += 1

    # Determine the Prakruti type based on counts
    if vata_count > pitta_count and vata_count > kapha_count:
        prakruti_type = "Vata"
    elif pitta_count > vata_count and pitta_count > kapha_count:
        prakruti_type = "Pitta"
    elif kapha_count > vata_count and kapha_count > pitta_count:
        prakruti_type = "Kapha"
    elif pitta_count == vata_count:
        prakruti_type = 'vata-pitta'
    elif pitta_count == kapha_count:
        prakruti_type = 'pitta-kapha'
    elif kapha_count == vata_count:
        prakruti_type = 'vata-kapha'
    else:
        prakruti_type = 'vata-pitta-kapha'

    return jsonify({'prakruti_type': prakruti_type})

if __name__ == '__main__':
    app.run(debug=True)
