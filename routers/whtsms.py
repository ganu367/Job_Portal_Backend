from fastapi import APIRouter, Depends, status, HTTPException, Response, Form, UploadFile, File
import database
from routers import alerts
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
import os
import database
import os
from dotenv import dotenv_values
from dotenv import load_dotenv
import requests
import json

config = dotenv_values(".env")
connect = load_dotenv()

get_db = database.get_db

router = APIRouter()


def sendSms(mobNo: int, template_name: str):
    try:

        url = "https://graph.facebook.com/v15.0/101908249520909/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": mobNo,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "en"
                }
            }
        })
        headers = {
            'Authorization': 'Bearer EAAKt2jgfn2IBADVpwZCa91gZCvc5LdFHRQnJHnrABxtL6VqM3UD80iZC5QFpZAZAD0ifTW5xvbwdkNzJaxkBOtRvHVvqEk61OHoKj2mhXqGvZA4FhCJpE0JKenHLGuZBJKXzQXg1VawNrwTbXlZAtgL56ltn1o4qWQd14QJecd7qXa0ZAIiEQ2MCZBoaF1ejFDZAqi8kZADbfPC8jgZDZD',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    except Exception as e:
        print(e)
