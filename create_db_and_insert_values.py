from gameServer import db
from gameServer.models import Card, Machine, Game, Game_result, Event_log, Event_type

#remove tables
db.drop_all()

#create tables
db.create_all()

#### Cards ####
cards = []
cards.append(Card(serial_number='00000101'))
cards.append(Card(serial_number='00000102'))
cards.append(Card(serial_number='00000103'))

for card in cards:
    db.session.add(card)


#### Machines ####
machines = []
machines.append(Machine())
machines.append(Machine())

for machine in machines:
    db.session.add(machine)


#### Games ####
games = []
games.append(Game(name="Poker"))
games.append(Game(name="Alchemy"))
games.append(Game(name="Super Joker 40"))


for game in games:
    db.session.add(game)



#### Event types ####
events = []
events.append(Event_type(name="login"))
events.append(Event_type(name="logout"))
events.append(Event_type(name="game_enter"))
events.append(Event_type(name="game_exit"))

for event in events:
    db.session.add(event)


db.session.commit()

