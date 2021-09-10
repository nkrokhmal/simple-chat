from app.imports.external import *
from sqlalchemy.orm import backref


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = self.hash_pass(value)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @staticmethod
    def hash_pass(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwd_hash = binascii.hexlify(pwd_hash)
        return salt + pwd_hash

    @staticmethod
    def verify_pass(provided_password, stored_password):
        stored_password = stored_password.decode('ascii')
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwd_hash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
        return pwd_hash == stored_password


@login_manager.user_loader
def user_loader(id):
    return db.session.query(User).filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = db.session.query(User).filter_by(username=username).first()
    return user if user else None


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    text = db.Column(db.String)
    time = db.Column(db.DateTime)

    group_id = db.Column(db.Text(length=36), db.ForeignKey("groups.id"), nullable=True)
    chat_id = db.Column(db.Text(length=36), db.ForeignKey("chats.id"), nullable=True)

    def __init__(self, *args, **kwargs):
        self.time = datetime.now()


user_group = db.Table(
    "user_group",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("group_id", db.Text(length=36), db.ForeignKey("groups.id"), primary_key=True),
)

admin_group = db.Table(
    "admin_group",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("group_id", db.Text(length=36), db.ForeignKey("groups.id"), primary_key=True),
)


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)
    time = db.Column(db.DateTime)

    users = db.relationship("User", secondary=user_group, backref="groups", lazy='subquery',)
    admins = db.relationship("User", secondary=admin_group, backref="admins", lazy='subquery')
    messages = db.relationship("Message", backref=backref("group"), lazy='subquery',)

    @staticmethod
    def create_group(name, user):
        group = Group(
            name=name,
            time=datetime.now()
        )
        group.users.append(user)
        group.admins.append(user)
        db.session.add(group)
        db.session.commit()


user_chat = db.Table(
    "user_chat",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("chat_id", db.Text(length=36), db.ForeignKey("chats.id"), primary_key=True),
)


class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    time = db.Column(db.DateTime)

    users = db.relationship("User", secondary=user_chat, backref="chats", lazy='subquery',)
    messages = db.relationship("Message", backref=backref("chat"), lazy='subquery',)

    @staticmethod
    def create_chat(users):
        assert len(users) == 2

        chat = Chat(time=datetime.now())
        chat.users.append(users)

        db.session.add(chat)
        db.session.commit()



