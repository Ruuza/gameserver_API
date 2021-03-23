'''utils.py: Usefull functions to help with data processing '''
import json
import random
from pymysql import NULL, STRING
from gameServer.models import Game, Card, Machine, Event_log, Event_type, Game_result
from gameServer import db


machines_in_games = {}

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

        returns: True if machine exists
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

        returns: True if card exists
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

        returns: id of the card
    '''

    card = Card.query.filter_by(serial_number=card_serial_number).first()

    return card.id


def is_card_in_machine(machine_id, card_serial_number):
    '''
        Check if the card is in the machine

        returns: True if card is in the machine
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

        returns: None if succesfully logout, else returns return message
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

        returns: None if succesfully logout, else returns return message
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

        returns: True when success
    '''

    event = Event_log(event_id=event_type_id, machine_id=machine_id, card_id=card_id)

    db.session.add(event)
    db.session.commit()

    return True

def is_game(game_id):
    '''
        Check if game_id is in database

        returns: True if game_id is in database, False if not
    '''

    game = Game.query.get(game_id)

    if game is None:
        return False
    else:
        return True


def enter_game(machine_id, game_id):
    '''
        Enter the game

        returns: True when success
    '''

    if not is_machine:
        raise ValueError("Machine ID don't exists!")

    if machine_id in machines_in_games.keys():
        raise SystemError("Machine is already in some game! Leave it")
    
    if not is_game(game_id):
        raise ValueError("Game ID don't exists!")
    
    log_event(3, machine_id, Machine.query.get(machine_id).card_id)
    machines_in_games[machine_id] = game_id

    


def exit_game(machine_id, game_id):
    '''
        Leave the game

        returns: True when success
    '''

    if not is_machine:
        raise ValueError("Machine ID don't exists!")

    if machine_id not in machines_in_games.keys():
        raise SystemError("Machine is not in the game!")

    if game_id != machines_in_games[machine_id]:
        raise ValueError("This game ID is not a current game on this machine!")
    else:
        log_event(4, machine_id, Machine.query.get(machine_id).card_id)
        machines_in_games.pop(machine_id)


def get_current_game(machine_id):
    '''
        Returns id of the current game, that is running on machine

        returns: ID of the game. None if there is no game on machine
    '''
    if machine_id in machines_in_games.keys():
        return machines_in_games[machine_id]
    else:
        return None

def spin(machine_id, bet, timestamp):
    '''
        Checks if machine is in the game and there is a card logged in and then do the spin.

        returns: ID of the game. None if there is no game on machine
    '''

    if( int(bet) not in [1, 2, 5, 10, 20, 50, 100]):
        raise ValueError("bet is not a acceptable number! Acceptable numbers are: [1, 2, 5, 10, 20, 50, 100]")
    
    machine = Machine.query.get(machine_id)
    card_id = machine.card_id
    
    if card_id is None:
        raise SystemError("There is no card associated with this machine!")

    game_id = get_current_game(machine_id)

    if game_id is None:
        raise SystemError("Machine is not in the game!")

    
    random_flip = random.uniform(0,1)

    if random_flip > 0.5:

        value_list = [1.5, 2.0, 2.5, 3.0]
        random_number = random.choice(value_list)
        bet = int(bet)

        win = bet * random_number
    
    else:

        win = 0

    game_result = Game_result(created_datetime=timestamp, bet=bet, win=win, machine_id=machine_id, card_id=card_id, game_id=game_id)
    db.session.add(game_result)
    db.session.commit()

