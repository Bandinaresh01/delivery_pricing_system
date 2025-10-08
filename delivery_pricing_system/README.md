# Delivery Pricing System

## Overview
The Delivery Pricing System is a FastAPI-based application designed to calculate delivery prices based on various parameters. It integrates with external APIs such as Google Maps for distance calculations and Twilio for notifications. The system supports user management, request handling, and escalation workflows.

## Features
- Calculate delivery prices using distance and other factors
- User and request management with database models
- Integration with Google Maps API for distance calculations
- Integration with Twilio API for SMS notifications
- Workflow orchestration using LangGraph
- RESTful API endpoints with FastAPI
- Frontend interface with HTML, CSS, and JavaScript for user interaction

## Project Structure
- `app/` - Main application code
  - `config.py` - Configuration and environment variables
  - `models.py` - Database models (User, Request, Escalation)
  - `utils.py` - Utility functions for API integrations
  - `graph.py` - LangGraph workflow definitions
  - `main.py` - FastAPI application and routes
- `static/` - Static files (CSS, JS)
- `test_demo.py` - Demo script for testing workflow
- `test_api.py` - API endpoint tests
- `test_api_edge_cases.py` - Edge case tests for API
- `requirements.txt` - Python dependencies
- `Procfile` - For deployment configuration
- `runtime.txt` - Python runtime version

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Bandinaresh01/delivery_pricing_system.git
   cd delivery_pricing_system
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
Start the FastAPI server with:
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Access the API documentation at `http://localhost:8000/docs`.

## Testing
Run the test scripts to verify functionality:
```
python test_demo.py
python test_api.py
python test_api_edge_cases.py
```

## Deployment
The project includes a `Procfile` and `runtime.txt` for deployment on platforms like Heroku.

## Contributing
Contributions are welcome. Please fork the repository and create a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact the maintainer.
