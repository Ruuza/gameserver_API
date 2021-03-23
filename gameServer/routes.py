from flask import url_for, redirect
from werkzeug.utils import escape
from gameServer import app, db
from gameServer.utils import generate_error_reply_JSON, generate_list_of_games_reply_JSON, generate_success_reply_JSON, validate_card_serial_number, validate_card_serial_number, is_machine, is_card, card_login, card_logout, is_card_in_machine
from gameServer.models import Card


machines = {}


@app.route("/cards/<string:card_serial_number>/register", methods=['POST'])
def register_card(card_serial_number):

    try:
        validation_result = validate_card_serial_number(card_serial_number)
        if  validation_result is not None:
            return str(generate_error_reply_JSON(validation_result))

        try:
            new_card = Card(serial_number=card_serial_number)
            db.session.add(new_card)
            db.session.commit()
        except:
            return str(generate_error_reply_JSON("Problem occured inserting card in database"))


        return str(generate_success_reply_JSON())

    except:
        return str(generate_error_reply_JSON("Something went wrong!"))
    


@app.route("/machines/<int:machine_id>/cards/<int:card_serial_number>/login", methods=['POST'])
def login_card_into_machine(machine_id, card_serial_number):
    try:

        if not is_machine(machine_id):
            return str(generate_error_reply_JSON("machine with that id don't exists!"))
        
        if not is_card(card_serial_number):
            return str(generate_error_reply_JSON("this card don't exists!"))

        
        card_login(machine_id, card_serial_number)

        return str(generate_success_reply_JSON())
    
    except:
        return str(generate_error_reply_JSON("Something went wrong"))


@app.route("/machines/<int:machine_id>/cards/<int:card_serial_number>/logout", methods=['POST'])
def logout_card_from_machine(machine_id, card_serial_number):
    try:

        if not is_machine(machine_id):
            return str(generate_error_reply_JSON("machine with that id don't exists!"))
        
        if not is_card(card_serial_number):
            return str(generate_error_reply_JSON("this card don't exists!"))

        if not is_card_in_machine(machine_id, card_serial_number):
            return str(generate_error_reply_JSON("card is not in machine!"))

        card_logout(machine_id)

        return str(generate_success_reply_JSON())
    
    except:
        return str(generate_error_reply_JSON("Something went wrong"))



@app.route("/machines/<int:machine_id>/games", methods=['GET'])
def get_games(machine_id):
    try:

        if not is_machine(machine_id):
            return str(generate_error_reply_JSON("machine with that id don't exists!"))
        
        return str(generate_list_of_games_reply_JSON(machine_id))
    
    except Exception as e:
        return str(generate_error_reply_JSON("Something went wrong"))

