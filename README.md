# EventEase 🗓️ - Your Ultimate Event Management Platform

**EventEase** is a beautifully designed event management platform that empowers users to discover, create, and manage events effortlessly. With robust features and a sleek interface, EventEase makes event planning a breeze.

## ✨ Key Features

### **Event Discovery & Management**
- 🗓️ **Event Listings**: Browse upcoming events with date, location, and category filters  
- 🔎 **Smart Search**: Find events by name, category, or location with instant results  
- 🖼️ **Visual Display**: Choose between list, grid, or calendar views  
- 📝 **Event Details**: View comprehensive event descriptions, locations, and attendee counts  

### **User Experience**
- 🔐 **Secure Auth**: Bcrypt-hashed passwords and Flask-Login sessions  
- ❤️ **Save Events**: Bookmark favorite events for quick access  
- 👥 **User Profiles**: Manage your events and saved favorites  
- 📱 **Mobile-Friendly**: Responsive design works on all devices  

### **Event Creation Tools**
- 🎚 **Easy Creation**: Simple forms for adding new events  
- ✏️ **Live Editing**: Update event details anytime  
- 🗑️ **One-Click Deletion**: Remove events when needed  

## 🛠️ Tech Stack

| Category       | Technologies                                                                 |
|----------------|-----------------------------------------------------------------------------|
| **Frontend**   | Flask, JavaScript, FontAwesome                          |
| **Backend**    | Python, Flask, Flask-Login, Flask-WTF                                       |
| **Database**   | MongoDB (PyMongo)                                                           |
| **Security**   | Bcrypt password hashing                                 |
                               
## 🚀 Quick Start
  
  ```bash
  # 1. Clone repo
  git clone https://github.com/yourusername/EventEase.git
  cd EventEase
  
  # 2. Setup virtual environment
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  
  # 3. Install dependencies
  pip install -r requirements.txt
  
  # 4. Configure environment
  echo "MONGO_URI=mongodb://localhost:27017/eventease" > .env
  echo "SECRET_KEY=your_random_key_here" >> .env
  
  # 5. Run!
  flask run
   ```

## 🌟 Why EventEase?

🏆 Winning Design: Bootstrap-powered responsive UI

⚡ Blazing Fast: MongoDB ensures quick data access

🔒 Bank-Grade Security: Bcrypt password protection

🧩 Extensible: Easy to add new features

