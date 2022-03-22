from app import db, session, Base


class Store(Base):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
