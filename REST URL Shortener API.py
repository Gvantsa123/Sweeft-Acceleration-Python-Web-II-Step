from flask import Flask, jsonify, redirect, request
import string
import random
import datetime

app = Flask(__name__)
urls = {}

def generate_short_code():
    # Generate a random short code of length 10 using lowercase letters and digits
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def is_valid_url(url):
    # Validate that the URL provided is a valid URL and has a length below 250 characters
    if len(url) > 250:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def create_url(short_code, url):
    # Create a new URL mapping and store it in the urls dictionary
    urls[short_code] = {
        'url': url,
        'created_at': datetime.datetime.utcnow(),
        'hits': 0
    }

@app.route('/shorten', methods=['POST'])
def shorten_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not is_valid_url(url):
        return jsonify({'error': 'Invalid URL'}), 400
    short_code = generate_short_code()
    create_url(short_code, url)
    return jsonify({'short_code': short_code})

@app.route('/shorten/<custom>', methods=['POST'])
def shorten_custom_url(custom):
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    if not is_valid_url(url):
        return jsonify({'error': 'Invalid URL'}), 400
    if custom in urls:
        return jsonify({'error': 'Custom name already exists'}), 400
    create_url(custom, url)
    return jsonify({'short_code': custom})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code not in urls:
        return jsonify({'error': 'Short code not found'}), 404
    urls[short_code]['hits'] += 1
    return redirect(urls[short_code]['url'], code=302)

@app.route('/stats/<short_code>')
def get_stats(short_code):
    if short_code not in urls:
        return jsonify({'error': 'Short code not found'}), 404
    return jsonify({
        'url': urls[short_code]['url'],
        'created_at': urls[short_code]['created_at'].strftime('%Y-%m-%d %H:%M:%S UTC'),
        'hits': urls[short_code]['hits']
    })

def delete_old_urls():
    # Delete any URLs that are older than 30 days
    now = datetime.datetime.utcnow()
    for short_code, url_data in urls.copy().items():
        created_at = url_data['created_at']
        if (now - created_at).days > 30:
            del urls[short_code]

if __name__ == '__main__':
    app.run(debug=True)

# Run a job to delete old URLs every day at midnight
scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_urls, 'cron', hour=0)
scheduler.start()