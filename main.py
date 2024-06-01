from flask import Flask, request, jsonify, send_from_directory
import json
from firestore import FirestoreConfig
from skills_service import Skills_Service

firestore_config = FirestoreConfig()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    hello = {"return": "Hello World!"}
    json_dump = json.dumps(hello)
    return json_dump

@app.route('/skill-trend-report', methods=['POST'])
def skill_trend_report():
    data = request.form
    skill = data.get('skill')
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    jsonParams = {'skill':skill, 'startDate':startDate, 'endDate':endDate}

    if not firestore_config.get_document(jsonParams):   
        skill_data = Skills_Service.getSkillData(skill, startDate, endDate)
        firestore_config.add_document(skill_data)
        return jsonify(skill_data)

    return firestore_config.get_document(jsonParams)
   

if __name__ == '__main__':
    app.run(port=7777)
