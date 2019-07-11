from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# use chrome_driver(ver74)
import chromedriver_binary
import os, datetime, json

from src.models import WebSite, Image
from src.modules.Colors import Colors
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
