from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), default='student')  # admin, teacher, student
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    xodim = db.relationship('Xodim', backref='user', uselist=False, lazy=True)
    ilmiy_ishlar = db.relationship('IlmiyIsh', backref='muallif', lazy=True)
    uslubiy_ishlar = db.relationship('UslubiyIsh', backref='muallif', lazy=True)
    fanlar = db.relationship('Fan', backref='muallim', lazy=True)
    yangiliklar = db.relationship('Yangilik', backref='muallif', lazy=True)
    izohlar = db.relationship('Izoh', backref='muallif', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Xodim(db.Model):
    __tablename__ = 'xodimlar'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lavozim = db.Column(db.String(100))
    ilmiy_daraja = db.Column(db.String(50))
    telefon = db.Column(db.String(20))
    bio = db.Column(db.Text)
    photo_path = db.Column(db.String(200))   # uploaded file
    kafedra = db.Column(db.String(150))
    ilmiy_unvon = db.Column(db.String(100))

    def __repr__(self):
        return f'<Xodim {self.user.full_name if self.user else self.id}>'


class IlmiyIsh(db.Model):
    __tablename__ = 'ilmiy_ishlar'
    id = db.Column(db.Integer, primary_key=True)
    sarlavha = db.Column(db.String(300), nullable=False)
    muallif_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hammuallif = db.Column(db.String(300))
    tur = db.Column(db.String(50), nullable=False)
    yil = db.Column(db.Integer, nullable=False)
    nashr_joyi = db.Column(db.String(200))
    doi_link = db.Column(db.String(200))
    fayl_path = db.Column(db.String(200))
    tavsif = db.Column(db.Text)
    holat = db.Column(db.String(30), default='kutilmoqda')
    views_count = db.Column(db.Integer, default=0)
    downloads_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    izohlar = db.relationship('Izoh', backref='ilmiy_ish',
                              lazy=True, foreign_keys='Izoh.ilmiy_ish_id')

    def __repr__(self):
        return f'<IlmiyIsh {self.sarlavha[:50]}>'


class UslubiyIsh(db.Model):
    __tablename__ = 'uslubiy_ishlar'
    id = db.Column(db.Integer, primary_key=True)
    sarlavha = db.Column(db.String(300), nullable=False)
    muallif_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hammuallif = db.Column(db.String(300))
    tur = db.Column(db.String(50), nullable=False)
    fan_nomi = db.Column(db.String(150))
    yil = db.Column(db.Integer, nullable=False)
    nashriyot = db.Column(db.String(200))
    fayl_path = db.Column(db.String(200))
    tavsif = db.Column(db.Text)
    holat = db.Column(db.String(30), default='kutilmoqda')
    views_count = db.Column(db.Integer, default=0)
    downloads_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    izohlar = db.relationship('Izoh', backref='uslubiy_ish',
                              lazy=True, foreign_keys='Izoh.uslubiy_ish_id')

    def __repr__(self):
        return f'<UslubiyIsh {self.sarlavha[:50]}>'


class Fan(db.Model):
    __tablename__ = 'fanlar'
    id = db.Column(db.Integer, primary_key=True)
    nomi = db.Column(db.String(200), nullable=False)
    kodi = db.Column(db.String(30))
    muallim_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    kredit = db.Column(db.Integer)
    soatlar = db.Column(db.Integer)
    semestr = db.Column(db.Integer)
    kurs = db.Column(db.Integer)
    mutaxassislik = db.Column(db.String(150))
    tavsif = db.Column(db.Text)

    def __repr__(self):
        return f'<Fan {self.nomi}>'


class Yangilik(db.Model):
    __tablename__ = 'yangiliklar'
    id = db.Column(db.Integer, primary_key=True)
    sarlavha = db.Column(db.String(250), nullable=False)
    matn = db.Column(db.Text, nullable=False)
    muallif_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rasm_url = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Yangilik {self.sarlavha[:50]}>'


class Izoh(db.Model):
    __tablename__ = 'izohlar'
    id = db.Column(db.Integer, primary_key=True)
    matn = db.Column(db.Text, nullable=False)
    muallif_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ilmiy_ish_id = db.Column(db.Integer, db.ForeignKey('ilmiy_ishlar.id'), nullable=True)
    uslubiy_ish_id = db.Column(db.Integer, db.ForeignKey('uslubiy_ishlar.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Izoh {self.id}>'
