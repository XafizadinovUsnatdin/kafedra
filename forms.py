from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SelectField, TextAreaField,
                     IntegerField, BooleanField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Foydalanuvchi nomi', validators=[DataRequired()])
    password = PasswordField('Parol', validators=[DataRequired()])
    remember = BooleanField('Eslab qolish')
    submit = SubmitField('Kirish')


class RegisterForm(FlaskForm):
    full_name = StringField("To'liq ism", validators=[DataRequired(), Length(min=3, max=150)])
    username = StringField('Foydalanuvchi nomi', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Parolni tasdiqlang', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('student', 'Talaba'), ('teacher', "O'qituvchi")])
    submit = SubmitField("Ro'yxatdan o'tish")


class IlmiyIshForm(FlaskForm):
    sarlavha = StringField('Sarlavha', validators=[DataRequired(), Length(max=300)])
    hammuallif = StringField('Hammuallif(lar)', validators=[Optional(), Length(max=300)])
    tur = SelectField('Turi', choices=[
        ('maqola', 'Ilmiy maqola'),
        ('monografiya', 'Monografiya'),
        ('patent', 'Patent / Ixtiro'),
        ('dissertatsiya', 'Dissertatsiya'),
        ('tezis', 'Konferensiya tezisi'),
    ])
    yil = IntegerField('Nashr yili', validators=[DataRequired(), NumberRange(min=1990, max=2030)])
    nashr_joyi = StringField('Nashr joyi (jurnal/nashriyot)', validators=[Optional(), Length(max=200)])
    doi_link = StringField('DOI yoki havola', validators=[Optional(), Length(max=200)])
    fayl = FileField('Fayl yuklash (PDF, DOC)', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Faqat PDF yoki Word fayllari!')
    ])
    tavsif = TextAreaField('Qisqacha tavsif', validators=[Optional()])
    submit = SubmitField('Saqlash')


class UslubiyIshForm(FlaskForm):
    sarlavha = StringField('Sarlavha', validators=[DataRequired(), Length(max=300)])
    hammuallif = StringField('Hammuallif(lar)', validators=[Optional(), Length(max=300)])
    tur = SelectField('Turi', choices=[
        ('darslik', 'Darslik'),
        ('oqquv_qollanma', "O'quv qo'llanma"),
        ('uslubiy_qollanma', "Uslubiy qo'llanma"),
        ('dastur', "O'quv dastur"),
        ('sillabusi', 'Sillabusi'),
    ])
    fan_nomi = StringField('Fan nomi', validators=[Optional(), Length(max=150)])
    yil = IntegerField('Yil', validators=[DataRequired(), NumberRange(min=1990, max=2030)])
    nashriyot = StringField('Nashriyot', validators=[Optional(), Length(max=200)])
    fayl = FileField('Fayl yuklash (PDF, DOC)', validators=[
        FileAllowed(['pdf', 'doc', 'docx'], 'Faqat PDF yoki Word fayllari!')
    ])
    tavsif = TextAreaField('Qisqacha tavsif', validators=[Optional()])
    submit = SubmitField('Saqlash')


class FanForm(FlaskForm):
    nomi = StringField('Fan nomi', validators=[DataRequired(), Length(max=200)])
    kodi = StringField('Fan kodi', validators=[Optional(), Length(max=30)])
    kredit = IntegerField('Kreditlar soni', validators=[Optional(), NumberRange(min=1, max=10)])
    soatlar = IntegerField('Soatlar soni', validators=[Optional(), NumberRange(min=1, max=500)])
    semestr = SelectField('Semestr', choices=[
        (1, '1-semestr'), (2, '2-semestr'), (3, '3-semestr'), (4, '4-semestr'),
        (5, '5-semestr'), (6, '6-semestr'), (7, '7-semestr'), (8, '8-semestr'),
    ], coerce=int)
    kurs = SelectField('Kurs', choices=[
        (1, '1-kurs'), (2, '2-kurs'), (3, '3-kurs'), (4, '4-kurs')
    ], coerce=int)
    mutaxassislik = StringField('Mutaxassislik', validators=[Optional(), Length(max=150)])
    tavsif = TextAreaField('Tavsif', validators=[Optional()])
    submit = SubmitField('Saqlash')


class YangilikForm(FlaskForm):
    sarlavha = StringField('Sarlavha', validators=[DataRequired(), Length(max=250)])
    matn = TextAreaField('Matn', validators=[DataRequired()])
    is_published = BooleanField('Nashr qilish')
    submit = SubmitField('Saqlash')


class XodimForm(FlaskForm):
    lavozim = SelectField('Lavozim', choices=[
        ('professor', 'Professor'),
        ('dotsent', 'Dotsent'),
        ('katta_oqituvchi', "Katta o'qituvchi"),
        ('assistent', 'Assistent'),
        ('mustaqil_izlanuvchi', 'Mustaqil izlanuvchi'),
    ])
    ilmiy_daraja = SelectField("Ilmiy daraja", choices=[
        ('yoq', "Yo'q"),
        ('phd', 'PhD (Falsafa doktori)'),
        ('dsc', 'DSc (Fan doktori)'),
    ])
    ilmiy_unvon = SelectField("Ilmiy unvon", choices=[
        ('yoq', "Yo'q"),
        ('dotsent', 'Dotsent'),
        ('professor', 'Professor'),
    ])
    kafedra = StringField('Kafedra', validators=[Optional(), Length(max=150)])
    telefon = StringField('Telefon', validators=[Optional(), Length(max=20)])
    bio = TextAreaField('Biografiya', validators=[Optional()])
    photo = FileField('Profil rasmi (JPG, PNG)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Faqat rasm fayllari!')
    ])
    submit = SubmitField('Saqlash')


class SettingsForm(FlaskForm):
    full_name = StringField("To'liq ism", validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Joriy parol', validators=[Optional()])
    new_password = PasswordField('Yangi parol', validators=[Optional(), Length(min=6)])
    new_password2 = PasswordField('Yangi parolni tasdiqlang',
                                  validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField('Saqlash')


class IzohForm(FlaskForm):
    matn = TextAreaField('Izoh', validators=[DataRequired(), Length(min=3, max=1000)])
    submit = SubmitField('Izoh qoldirish')
