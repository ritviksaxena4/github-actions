from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GITHUB_API_BASE = "https://api.github.com"

@app.route('/<username>', methods=['GET'])
def get_gists(username):
    
    try:
        if not username or not isinstance(username, str):
            return jsonify({
                "error": "Invalid username provided",
                "status": "error"
            }), 400
        
        
        api_url = f"{GITHUB_API_BASE}/users/{username}/gists"
        
        response = requests.get(api_url, timeout=5)
        if response.status_code == 404:
            return jsonify({
                "error": f"User '{username}' not found",
                "status": "error"
            }), 404
        
        if response.status_code != 200:
            return jsonify({
                "error": f"GitHub API returned status {response.status_code}",
                "status": "error"
            }), response.status_code
        
        
        gists = response.json()
        
        
        if not gists:
            return jsonify({
                "username": username,
                "gists": [],
                "count": 0,
                "message": "No public gists found for this user"
            }), 200
        
        
        formatted_gists = []
        for gist in gists:
            formatted_gists.append({
                "id": gist.get("id"),
                "url": gist.get("url"),
                "html_url": gist.get("html_url"),
                "description": gist.get("description", "No description"),
                "created_at": gist.get("created_at"),
                "updated_at": gist.get("updated_at"),
                "files": list(gist.get("files", {}).keys())
            })
        
        return jsonify({
            "username": username,
            "gists": formatted_gists,
            "count": len(formatted_gists),
            "status": "success"
        }), 200
    
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching gists for {username}")
        return jsonify({
            "error": "GitHub API request timed out",
            "status": "error"
        }), 503
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching gists: {str(e)}")
        return jsonify({
            "error": f"Error fetching data from GitHub: {str(e)}",
            "status": "error"
        }), 503
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "error"
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    }), 200


@app.route('/', methods=['GET'])
def welcome():
    """Welcome message"""
    return jsonify({
        "message": "Welcome to GitHub Gists API",
        "usage": "GET /<username> to fetch gists for a user",
        "example": "GET /octocat"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
