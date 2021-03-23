from datetime import datetime
from gameServer import db

class Machine(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Machine('{self.id}')"

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(20), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    machines = db.relationship('Machine', backref='card_in_usage', lazy=True)

    def __repr__(self):
        return f"Card('{self.serial_number}', '{self.created_datetime}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Game('{self.name}')"


class Game_result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bet = db.Column(db.Integer, nullable=False)
    win = db.Column(db.Boolean, nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return f"Game_result('{self.bet}', '{self.win}', '{self.machine_id}', '{self.card_id}', '{self.game_id}', '{self.created_datetime}')"


class Event_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event_type.id'), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)

    def __repr__(self):
        return f"Event_log('{self.event_id}', '{self.machine_id}', '{self.card_id}', '{self.created_datetime}')"


class Event_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Event_type('{self.name}')"
