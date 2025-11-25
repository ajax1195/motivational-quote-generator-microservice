from flask import Flask, jsonify, request
import random

app = Flask(__name__)

API_VERSION = "v1"

QUOTES = [
    {"text": "The secret of getting ahead is getting started.", "author": "Mark Twain", "category": "productivity", "lang": "en"},
    {"text": "It always seems impossible until it’s done.", "author": "Nelson Mandela", "category": "perseverance", "lang": "en"},
    {"text": "You miss 100% of the shots you don’t take.", "author": "Wayne Gretzky", "category": "courage", "lang": "en"},
    {"text": "Small steps every day.", "author": "Unknown", "category": "habit", "lang": "en"},
    {"text": "Fall seven times, stand up eight.", "author": "Japanese Proverb", "category": "perseverance", "lang": "en"},
]

def validate_query_params(args):
    """
    Validate the allowed parameters for the /quote endpoint.
    """
    allowed = {"category", "lang"}
    for key in args.keys():
        if key not in allowed:
            return None, None, ("UNSUPPORTED_PARAMETER", "Only 'category' and 'lang' are supported.", 400)

    category = args.get("category")
    lang = args.get("lang")
    return category, lang, None


def build_error_response(error_code, message, http_status):
    """Return a standardized error JSON response."""
    return jsonify({"error": error_code, "message": message}), http_status

def pick_quote(category=None, lang=None):
    pool = QUOTES
    if category:
        pool = [q for q in pool if q["category"].lower() == category.lower()]
    if lang:
        pool = [q for q in pool if q["lang"].lower() == lang.lower()]
    if not pool:
        return None
    return random.choice(pool)

@app.route(f"/{API_VERSION}/quote", methods=["GET"])
def get_quote():
    """
    GET /v1/quote?category={string}&lang={string}
    Returns: 200 JSON { quote, author, category, lang, service, version }
    Errors: 404 if no quote matches filters, 400 if unsupported params
    """
    category, lang, err = validate_query_params(request.args)
    if err:
        error_code, message, status = err
        return build_error_response(error_code, message, status)

    q = pick_quote(category, lang)
    if not q:
        return build_error_response("NOT_FOUND", "No quote matches the filters.", 404)

    return jsonify({
        "quote": q["text"],
        "author": q["author"],
        "category": q["category"],
        "lang": q["lang"],
        "service": "motivational-quote-generator",
        "version": API_VERSION
    }), 200

@app.route(f"/{API_VERSION}/categories", methods=["GET"])
def get_categories():
    cats = sorted({q["category"] for q in QUOTES})
    return jsonify({"categories": cats, "count": len(cats)}), 200

@app.route(f"/{API_VERSION}/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "motivational-quote-generator", "version": API_VERSION}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
