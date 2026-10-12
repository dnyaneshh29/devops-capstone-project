"""
Models for Account
"""
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Account.init_db(app)


class PersistentBase:
    """Base class with persistent methods"""

    def __init__(self):
        """Initialize base with id"""
        self.id = None  # pylint: disable=invalid-name

    def create(self):
        """Create an Account in the database"""
        logger.info("Creating %s", getattr(self, "name", None))
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update an Account in the database"""
        logger.info("Updating %s", getattr(self, "name", None))
        db.session.commit()

    def delete(self):
        """Delete an Account from the database"""
        logger.info("Deleting %s", getattr(self, "name", None))
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initialize the database session"""
        logger.info("Initializing database")
        cls.app = app
        db.init_app(app)
        app.app_context().push()
        db.create_all()

    @classmethod
    def all(cls):
        """Return all records"""
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Find a record by ID"""
        return cls.query.get(by_id)


class Account(db.Model, PersistentBase):
    """Class that represents an Account"""

    app = None

    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(256))
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.Date(), nullable=False, default=date.today())

    def __init__(self, id=None, name=None, email=None, address=None,
                 phone_number=None, date_joined=None):  # pylint: disable=too-many-arguments
        """Initialize Account with fields"""
        super().__init__()
        self.id = id
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.date_joined = date_joined or date.today()

    def __repr__(self):
        """String representation"""
        return f"<Account {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serialize Account to dict"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat()
        }

    def deserialize(self, data):
        """Deserialize Account from dict"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data["address"]
            self.phone_number = data.get("phone_number")
            date_joined = data.get("date_joined")
            self.date_joined = (
                date.fromisoformat(date_joined) if date_joined else date.today()
            )
        except KeyError as error:
            raise DataValidationError(
                "Invalid Account: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: bad or no data - " + error.args[0]
            ) from error
        return self
