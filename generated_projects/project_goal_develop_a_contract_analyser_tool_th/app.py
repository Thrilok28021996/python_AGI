from flask import Flask, request, jsonify
from contract_parser import parse_contract
from ollama_model import analyze_text
from results_formatter import format_results
from errors import handle_error

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get the contract document from the request
        if 'contract' not in request.files or not request.files['contract'].filename:
            raise ValueError("No file part or no file selected")
        
        contract_document = request.files['contract'].read().decode('utf-8')
        
        # Parse the contract document
        parsed_contract = parse_contract(contract_document)
        
        # Analyze the contract using Ollama models
        analysis_results = analyze_text(parsed_contract)
        
        # Save the analysis results to the database
        save_analysis_results(analysis_results)
        
        # Format the results for output
        formatted_results = format_results(analysis_results)
        
        return jsonify(formatted_results), 200
    except Exception as e:
        return handle_error(e), 400

if __name__ == '__main__':
    app.run(debug=True)