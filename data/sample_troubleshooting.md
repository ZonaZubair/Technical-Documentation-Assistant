# Python Project Troubleshooting

## Installation
Install the project dependencies with:

python -m pip install -r requirements.txt

## Running the Application
Start the Streamlit application with:

streamlit run app.py

## Common Issue: Missing Module
If Python reports that a module is missing, confirm that the virtual environment is activated and install the project dependencies again.

## Common Issue: API Key
If OpenAI requests fail because of authentication, check that OPENAI_API_KEY is correctly configured in the local .env file.
