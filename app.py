from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API credentials securely
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    job_title = request.form['job_title']
    
    url = f'https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}&results_per_page=10&what={job_title}&content-type=application/json'
    
    response = requests.get(url)
    
    try:
        data = response.json()
    except Exception as e:
        return render_template('result.html', jobs=[], job_title=job_title, error="Invalid response from API.")

    jobs = []
    for result in data.get('results', []):
        jobs.append({
            'title': result.get('title'),
            'company': result.get('company', {}).get('display_name'),
            'location': result.get('location', {}).get('display_name'),
            'salary': f"{result.get('salary_min', 0):,.0f} - {result.get('salary_max', 0):,.0f}" if result.get('salary_min') else "Not Provided",
            'redirect_url': result.get('redirect_url')
        })

    return render_template('result.html', jobs=jobs, job_title=job_title)

if __name__ == '__main__':
    app.run(debug=True)
