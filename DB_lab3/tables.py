import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Developer(Base):
    __tablename__ = 'developer'
    dev_id = db.Column(db.Integer, db.Sequence('developer_dev_id_seq'), primary_key=True)
    name = db.Column(db.String, primary_key=True)
    
    game_of_dev = db.orm.relationship("Videogame", secondary="dev_game")
    
    def __init__(self, dev_id, name):
        self.dev_id = dev_id
        self.name = name
        
    
    def __repr__(self):
        return (f'dev_id - {self.dev_id}\n'
                f'name - {self.name}')
                           

class Videogame(Base):
    __tablename__ = 'videogame'
    game_id = db.Column(db.Integer, db.Sequence('videogame_game_id_seq'), primary_key=True)
    v_name = db.Column(db.String)
    genre = db.Column(db.String)
    price = db.Column(db.Numeric)
    
    
    dev_of_game = db.orm.relationship("Videogame", secondary="dev_game")
    player_of_game = db.orm.relationship("Player", secondary="game_player") 
    
    def __init__(self, game_id, v_name, genre, price):
        self.game_id = game_id
        self.v_name = v_name
        self.genre = genre
        self.price = price
    
    def __repr__(self):
        return (f'game_id - {self.game_id}\n'
                f'v_name - {self.v_name}\n'
                f'genre - {self.genre}\n'
                f'price - {self.price}')
                    
                
class Player(Base):
    __tablename__ = 'player'
    id = db.Column(db.Integer, db.Sequence('player_id_seq'), primary_key=True)
    nickname = db.Column(db.String)

    game_of_player = db.orm.relationship("Videogame", secondary="game_player") 
    
    def __init__(self, id, nickname):
        self.id = id
        self.nickname = nickname

    
    def __repr__(self):
        return (f'id - {self.id}\n'
                f'nickname - {self.nickname}')
 
 
 
class Dev_Game(Base):
    __tablename__ = 'dev_game'    
    dev_id = db.Column(db.String, db.ForeignKey('developer.dev_id'))
    game_id = db.Column(db.String, db.ForeignKey('videogame.game_id'))
    release_date = db.Column(db.DateTime)
    
    dev_of_game = db.orm.relationship(Videogame, backref=db.orm.backref('dev_game', cascade="all, delete-orphan"))
    game_of_dev = db.orm.relationship(Developer, backref=db.orm.backref('dev_game', cascade="all, delete-orphan"))
    
    __table_args__ = (db.PrimaryKeyConstraint('dev_id', 'game_id', name='dev_game_pkey'),)
    
    def __init__(self, dev_id, game_id, release_date):
        self.dev_id = dev_id
        self.game_id = game_id
        self.release_date = release_date
    
    def __repr__(self):
        return (f'dev_id - {self.dev_id}\n'
                f'game_id - {self.game_id}\n'
                f'release_date - {self.release_date}')
 
 
class Game_Player(Base):
    __tablename__ = 'game_player'
    game_id = db.Column(db.String, db.ForeignKey('videogame.game_id'))
    player_id = db.Column(db.String, db.ForeignKey('player.id'))
    buy_date = db.Column(db.DateTime)


    game_of_player = db.orm.relationship(Player, backref=db.orm.backref('game_player', cascade="all, delete-orphan"))
    player_of_game = db.orm.relationship(Videogame, backref=db.orm.backref('game_player', cascade="all, delete-orphan"))
    
    __table_args__ = (db.PrimaryKeyConstraint('game_id', 'player_id', name='game_player_pkey'),)
    
    def __init__(self, game_id, player_id, buy_date):
        self.game_id = game_id
        self.player_id = player_id
        self.buy_date = buy_date
    
    def __repr__(self):
        return (f'game_id - {self.game_id}\n'
                f'player_id - {self.player_id}\n'
                f'buy_date - {self.buy_date}')
 
 