from flask import Flask, jsonify, request
from supreme_config import APP_NAME, PORT, SUPREME_ID, BUSINESS_ID, COMPANY_ID, PERSON_ID
from identity_service import get_supreme_profile, get_person_profile, search_entities

app = Flask(__name__)

# CORS support
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.get("/")
def root():
    return jsonify({
        "service": APP_NAME,
        "status": "running",
        "supreme_id": SUPREME_ID,
        "owner_person_id": PERSON_ID,
        "version": "1.0.0"
    }), 200

@app.get("/health")
def health():
    return jsonify({
        "service": APP_NAME,
        "status": "healthy",
        "supreme_id": SUPREME_ID,
        "owner_person_id": PERSON_ID
    }), 200

@app.get("/supreme/status")
def supreme_status():
    profile = get_supreme_profile()
    return jsonify({
        "service": APP_NAME,
        "status": "active",
        "supreme_id": profile["supreme_id"],
        "owner_person_id": profile["owner_person_id"],
        "business_id": BUSINESS_ID,
        "company_id": COMPANY_ID,
        "role": profile["role"]
    }), 200

@app.get("/supreme/profile")
def supreme_profile():
    return jsonify(get_supreme_profile()), 200

@app.get("/supreme/person")
def supreme_person():
    return jsonify(get_person_profile()), 200

@app.get("/supreme/search")
def supreme_search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({
            "error": "Missing q query parameter"
        }), 400

    results = search_entities(q)
    return jsonify({
        "query": q,
        "results": results,
        "count": len(results)
    }), 200

@app.get("/supreme/persons")
def persons_list():
    return jsonify({
        "service": APP_NAME,
        "people": [get_person_profile()]
    }), 200

@app.get("/supreme/businesses")
def businesses_list():
    return jsonify({
        "service": APP_NAME,
        "businesses": [{
            "business_id": BUSINESS_ID,
            "owner_person_id": PERSON_ID,
            "supreme_id": SUPREME_ID,
            "name": "RAJESH KHANDELWAL OFFICIAL",
            "display_name": "👑 RAJESH KHANDELWAL OFFICIAL 👑"
        }]
    }), 200

@app.get("/supreme/companies")
def companies_list():
    return jsonify({
        "service": APP_NAME,
        "companies": [{
            "company_id": COMPANY_ID,
            "owner_person_id": PERSON_ID,
            "business_id": BUSINESS_ID,
            "supreme_id": SUPREME_ID,
            "name": "DR RAJESH KHANDELWAL IBC",
            "display_name": "👑 DR RAJESH KHANDELWAL IBC 👑"
        }]
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Server error",
        "message": "Internal server error"
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
