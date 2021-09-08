from app.imports.external import *


class User(db.Document):
    email = db.StringField(required=True)
    name = db.StringField(required=True)
    password = db.StringField()

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


class Message(db.EmbeddedDocument):
    time = db.DateTimeField()
    text = db.StringField(max_length=200)
    author = db.ReferenceField(User)


class EmbeddedUser(db.EmbeddedDocument):
    email = db.StringField(required=True)
    name = db.StringField(required=True)

    @staticmethod
    def copy_user(user):
        return EmbeddedUser(
            email=user.email,
            name=user.name,
        )


class Room(db.Document):
    id = db.StringField()
    time = db.DateTimeField()
    name = db.StringField(required=True)
    author = db.ReferenceField(User)
    is_active = db.BooleanField()
    users = db.ListField(db.EmbeddedDocumentField(EmbeddedUser))
    messages = db.ListField(db.EmbeddedDocumentField(Message))

    @staticmethod
    def create_new_room(name, user):
        room = Room(
            id=uuid.uuid4().hex,
            name=name,
            is_active=True,
            time=datetime.now(),
        )
        room.users.append(
            EmbeddedUser.copy_user(user)
        )
        room.save()

    @staticmethod
    def create_personal_room(name, users):
        assert len(users) == 2

        # todo: think about rooms naming. Hash better?
        room = Room(
            id=uuid.uuid4().hex,
            name=f"{users[0].username}_{users[1].username}",
            is_active=True,
            time=datetime.now(),
        )

        for user in users:
            room.users.append(
                EmbeddedUser.copy_user(user)
            )
        room.save()





