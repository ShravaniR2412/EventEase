from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# API Configuration
API_BASE_URL = 'http://127.0.0.1:5000'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(f'{API_BASE_URL}/users/login', json={
            'username': request.form['username'],
            'password': request.form['password']
        })
        if response.status_code == 200:
            session['user'] = response.json()
            return render_template('otp.html', error='Registration failed')
        return render_template('login.html', error='Invalid credentials')
    
    # ✅ This handles GET properly
    
    return render_template('login.html')

 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Call your API to register
        response = requests.post(f'{API_BASE_URL}/users/register', json={
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password'],
            'bio': request.form['bio'],
            'profile_url': request.form['profile_url'],
        })
        if response.status_code == 201:
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/events')
def events_list():
    # Ensure user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect to login if no user is in session

    # Get user ID from session
    user_id = session['user'].get('id')
    
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if no user ID found in session

    # Fetch events for the logged-in user
    response = requests.get(f'{API_BASE_URL}/events/get?user_id={user_id}')
    
    if response.status_code == 200:
        events = response.json()
    else:
        events = []

    # Render the events list template with the fetched events
    return render_template('events/list.html', events=events)

@app.route('/events/grid')
def events_grid():
    # Ensure user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect to login if no user is in session

    # Get user ID from session
    user_id = session['user'].get('id')
    
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if no user ID found in session

    # Fetch events for the logged-in user
    response = requests.get(f'{API_BASE_URL}/events/get?user_id={user_id}')
    
    if response.status_code == 200:
        events = response.json()
    else:
        events = []

    # Render the events frid template with the fetched events
    return render_template('events/grid.html', events=events)

@app.route('/events/calendar')
def events_calendar():
    # Ensure user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect to login if no user is in session

    # Get user ID from session
    user_id = session['user'].get('id')
    
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if no user ID found in session

    # Fetch events for the logged-in user
    response = requests.get(f'{API_BASE_URL}/events/get?user_id={user_id}')
    
    if response.status_code == 200:
        events = response.json()
    else:
        events = []

    # Render the events calender template with the fetched events
    return render_template('events/calendar.html', events=events)

@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Extract data from the form
        data = {
            'name': request.form['name'],
            'date': request.form['date'],
            'location': request.form['location'],
            'description': request.form['description'],
            'category': request.form['category'],
            'image': request.form['image'],
            'time': request.form['time'],  # Added time field
            'created_by': session['user']['id']  # Passing user ID from session
        }

        # Make the POST request to the API to create an event
        response = requests.post(f'{API_BASE_URL}/events/create', json=data)

        if response.status_code == 201:
            return redirect(url_for('events_list'))  # Redirect to the events list page
        
        # If the API request fails, display an error message
        return render_template('events/create.html', error='Failed to create event')

    return render_template('events/create.html')

@app.route('/events/<event_id>')
def view_event(event_id):
    response = requests.get(f'{API_BASE_URL}/events/get/{event_id}')
    event = response.json() if response.status_code == 200 else None
    if not event:
        return redirect(url_for('events_list'))
    return render_template('events/view.html', event=event)


@app.route('/events/<event_id>/update', methods=['POST'])
def update_event(event_id):
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))

    # Get form data submitted from HTML form (not JSON!)
    form_data = {
        "name": request.form.get("name"),
        "date": request.form.get("date"),
        "time": request.form.get("time"),
        "location": request.form.get("location"),
        "description": request.form.get("description"),
        "image": request.form.get("image"),
        "category": request.form.get("category")
    }

    try:
        # Send the data to the API using POST
        response = requests.post(
            f"{API_BASE_URL}/events/update/{event_id}",
            json=form_data
        )
        if response.status_code == 200:
            return redirect(url_for('view_event', event_id=event_id))
        else:
            error = response.json().get('error', 'Update failed')
            return render_template("events/edit.html", event=form_data, error=error)
    except Exception as e:
        return render_template("events/edit.html", event=form_data, error=str(e))


   
@app.route('/events/<event_id>/edit', methods=['GET'])
def edit_event(event_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    # GET request: load event data
    try:
        response = requests.get(f"{API_BASE_URL}/events/get/{event_id}")
        if response.status_code == 200:
            event = response.json()
            return render_template("events/edit.html", event=event)
        else:
            return redirect(url_for('events_list'))
    except Exception as e:
        return f"Error fetching event: {e}", 500

@app.route('/events/<event_id>/delete', methods=['POST'])  # HTML forms support only GET/POST
def delete_event(event_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        # Call the backend DELETE API
        response = requests.delete(f"{API_BASE_URL}/events/delete/{event_id}")
        if response.status_code == 204:
            return redirect(url_for('events_list'))
        else:
            error = response.json().get('error', 'Failed to delete event')
            return f"Error: {error}", 400
    except Exception as e:
        return f"Exception occurred: {e}", 500

@app.route('/profile')
def user_profile():
    print("hi")
    if 'user' not in session:
        return redirect(url_for('login'))
    
    print("Session data:", session) 
    return render_template('user/profile.html', user=session['user'])

@app.route('/saved')
def saved_events():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    response = requests.get(f'{API_BASE_URL}/users/{session["user"]["id"]}/saved',
        headers={'Authorization': f'Bearer {session["user"]["token"]}'})
    
    events = response.json() if response.status_code == 200 else []
    return render_template('user/bookmark.html', events=events)

@app.route('/save_event/<event_id>', methods=['POST'])
def save_event(event_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    response = requests.post(f'{API_BASE_URL}/users/{session["user"]["id"]}/saved/{event_id}',
        headers={'Authorization': f'Bearer {session["user"]["token"]}'})
    
    return jsonify({'success': response.status_code == 200})



@app.route('/logout')
def logout():
    # Log the user out (e.g., clear session or logout mechanism)
    session.pop('user_id', None)  # Example: pop user_id from session
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)