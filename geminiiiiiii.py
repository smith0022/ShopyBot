import google.generativeai as genai
import os

genai.configure(api_key = 'AIzaSyD1a-t6qcECmlLup17EQS0tPPXprjONNo0')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)