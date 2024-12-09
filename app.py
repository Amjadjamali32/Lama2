from flask import Flask, request, jsonify
from langchain_groq import ChatGroq

app = Flask(__name__)

# Initialize the Llama model with the API key from the environment
import os
llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv('GROQ_API_KEY'),
    model_name="llama-3.1-70b-versatile"
)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    try:
        # Build the prompt
        prompt = f"""
        Generate a formal crime incident report with the following details:
        
        Report Number: [Auto-generate report number]
        
        Date and Time of Incident: {data['incident_date']} {data['incident_time']}
        Location: {data['location']}
        Incident Type: {data['incident_type']}
        Complainant Name: {data['complainant_name']}
        Complainant Contact Information:
        - Phone Number: {data['complainant_phone']}
        - Email: {data['complainant_email']}
        
        Incident Overview:  
        On {data['incident_date']} at approximately {data['incident_time']}, {data['complainant_name']} reported an incident involving {data['incident_type']} at {data['location']}.
        
        Incident Details:  
        {data['incident_description']}
        
        Actions Taken:  
        - Police Response: {data['police_response']}
        - Evidence Collected: {data['evidence_collected']}
        - Witnesses: [Insert any witness statements or details, if applicable]
        
        Additional Notes or Requests:  
        {data['additional_notes']}
        
        Signature of Complainant:  
        {data['complainant_name']}
        Date: [Insert Date of Report Submission]
        
        Please ensure the report is clear, formal, and professional.
        """
        
        # Get the response from Llama model
        response = llm.invoke(prompt)
        return jsonify({"report": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT env variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Start the server  
