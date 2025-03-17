from config import db, app, create_short_code
from models import Urls
from flask import request, jsonify
    

@app.route('/shorten', methods=["POST"])
def create_short_url():
    '''Create new short url'''
    url = request.json.get('url') # Get the url to be shortened
    
    if not url:
        return jsonify({'message': 'Please provide a url.'}), 401
    
    short_code = create_short_code() # Generate short code
    new_url = Urls(url=url, short_code=short_code) # Create new url object
    
    try:
        db.session.add(new_url) # Add new url to the database
        db.session.commit()
        return jsonify(new_url.to_json()), 201
    except Exception as e:
        return jsonify({'Error': f'{e}'}), 400
    

@app.route('/shorten/<string:short_code>', methods=["GET", "PUT", "DELETE"])
def show_long_url(short_code):
    '''Show the long url'''
    url = Urls.query.filter_by(short_code=short_code).first() # Check if the url exists in the database
    if not url:
        return jsonify({'message': 'Url not found'}), 404
    
    if request.method == "PUT":
        new_url = request.json.get('url') # Get the new url from the user
        if not new_url:
            return jsonify({'message': 'Please provide a new url'})
        url.url = new_url # Update the url in the database
        try:
            db.session.commit()
            return jsonify(url.to_json()), 200
        except Exception as e:
            return jsonify({'Error': f'{e}'}), 400
        
    if request.method == "DELETE":
        try:
            db.session.delete(url)
            db.session.commit()
            return jsonify(), 204
        except Exception as e:
            return jsonify({'Error': f'{e}'}), 400
    url.access_count += 1 # Increase te access count for the url
    db.session.commit()   
    return jsonify(url.to_json()), 200


@app.route('/shorten/<string:short_code>/stats', methods=["GET"])
def get_url_stats(short_code):
    '''Get the stats of the url'''
    url = Urls.query.filter_by(short_code=short_code).first() # Check if the url exists in the database
    if not url:
        return jsonify({'message': 'Url not found'}), 404
    
    return jsonify(url.to_json(include_access_count=True)), 200
     
  
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)