'''utils.py: Usefull functions to help with data processing '''
import json

from pymysql import NULL, STRING
from gameServer.models import Game, Card, Machine, Event_log, Event_type
from gameServer import db

def generate_error_reply_JSON(error_desc):
    '''
        Generate json string that will look like: {"sucess": 0, "error_desc":<error_desc>}
    '''
    dict = {}
    dict["success"] = 0
    dict["desc"] = error_desc
    return json.dumps(dict)


def generate_success_reply_JSON():
    '''
        Generate json string that will look like: {"sucess": 1}
    '''

    dict = {}
    dict["success"] = 1
    return json.dumps(dict)


def generate_list_of_games_reply_JSON(machine_id):
    '''
        Generate json string that will look like: {"sucess": 1, "games":{"game_id1": game_name1, "game_id2": game_name2}}
    '''
    

    dict = {}
    dict["success"] = 1

    games = Game.query.all()

    # Create games dictionary, where "game_id" is key and "game_name" is value 
    gamesDict = {}
    for game in games:
        gamesDict[game.id] = game.name

    dict["games"] = gamesDict

    return json.dumps(dict)


def validate_card_serial_number(card_serial_number):
    '''
        Validate, if it's valid card serial number

        card_serial_number: Serial number to be validated

        returns: None if success else returns error message
    '''

    if card_serial_number == "" or not isinstance(card_serial_number, str):
        return "Serial number can't be empty and has to be a string"


    if(len(card_serial_number) > 20):
        return "Serial number is too long (max is 20 chars)"

    if(Card.query.filter_by(serial_number=card_serial_number).first() != None):
        return "Card already exists"

    return None

def is_machine(machine_id):
    '''
        Check if machine exists

        return: True if machine exists
                Else if macine not exists
    '''

    machine = Machine.query.get(machine_id)

    if machine is None:
        return False
    else:
        return True

def is_card(card_serial_number):
    '''
        Check if the card exists

        return: True if card exists
                Else if card not exists
    '''

    card = Card.query.filter_by(serial_number=card_serial_number).first()

    if(card is None):
        return False
    else:
        return True

def get_card_id_by_serial_number(card_serial_number):
    '''
        Check id of the card by it's serial number

        return: id of the card
    '''

    card = Card.query.filter_by(serial_number=card_serial_number).first()

    return card.id


def is_card_in_machine(machine_id, card_serial_number):
    '''
        Check if the card is in the machine

        return: True if card is in the machine
                Else if not
    '''

    card = Card.query.filter_by(serial_number=card_serial_number).first()
    machine = Machine.query.get(machine_id)

    if card.id == machine.card_id:
        return True
    else:
        return False

    

def card_logout(machine_id):
    '''
        Logout the card from the machine. Card has to be logged and serial number has to match

        return: None if succesfully logout, else returns return message
    '''

    machine = Machine.query.get(machine_id)

    if (machine.card_id is None):
        return "There is no card logged in the machine!"

    log_event(2, machine_id, machine.card_id)

    machine.card_id = None
    db.session.commit()

def card_login(machine_id, card_serial_number):
    '''
        Login the card into the machine. If another card is already logged, logout the other before

        return: None if succesfully logout, else returns return message
    '''
    
    machine = Machine.query.get(machine_id)
    card_id = get_card_id_by_serial_number(card_serial_number)

    if(machine.card_id != None):
        card_logout(machine_id)
    
    log_event(1, machine_id, card_id)

    machine.card_id = card_id
    db.session.commit()


def log_event(event_type_id, machine_id, card_id):
    '''
        Logs the event

        return: True when success
    '''

    event = Event_log(event_id=event_type_id, machine_id=machine_id, card_id=card_id)

    db.session.add(event)
    db.session.commit()

    return True

