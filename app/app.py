###########
# Imports #
###########


# Database
import redis
# Flask web app
from flask import Flask, render_template, request, redirect, url_for


#############
# Classes #
#############


class StrListItem():
    """Holds item from database (index, value).
    """
    
    def __init__(self, index: int, string: str) -> None:
        self.index = index
        self.string = string


#############
# Variables #
#############


str_list_key = 'str_list'


#############
# Functions #
#############


def get_str_list() -> list:
    """Retrieves strings stored in database.
    """
    
    str_list = []
    for i in range(database.llen(str_list_key)):
        str_list.append(StrListItem(i, str(database.lindex(str_list_key, i), encoding='utf-8')))
    
    return str_list


def index_to_button(index: int) -> str:
    """Generates button name from given index.
    """
    
    return 'bitton_x_' + str(index)


def button_to_index(name: str) -> int:
    """Retrieves index from button name.
    """
    
    return int(name[9:])


def render_main_page() -> str:
    """Returns main page html.
    """
    
    return render_template('index.html', str_list=get_str_list(), index_to_button=index_to_button)


#######
# RUN #
#######


# Init flask app
app = Flask(__name__)
# Init database
database = redis.Redis(host='database', port=6379)


# Index page
@app.route('/', methods=['POST', 'GET'])
def index():
    # Redirect to home
    return redirect(url_for('home'))


# Main page
@app.route('/home', methods=['POST', 'GET'])
def home():
    # Input request
    if request.method == 'POST':
        if 'str_input' in request.form:
            database.lpush(str_list_key, request.form['str_input'])
        else:
            index = button_to_index(list(request.form.to_dict().keys())[0])
            # Shift values, removing desired one from list
            for i in range(index, 0, -1):
                database.lset(str_list_key, i, database.lindex(str_list_key, i-1))
            # Pop 0 element
            database.lpop(str_list_key)
        
        # Redirect to this page to confirm POST request 
        return redirect(url_for('home'))
    
    # Render home page        
    return render_main_page()