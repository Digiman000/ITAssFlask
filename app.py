"""is importing * best practice? No, am I going to do it? Yes
did I use too many modules? This is how flask + other sources tell me to do things
also no security because I have no time and refuse to use flaskWTF
Is this a good app? That's a matter of opinion, but it is my *first* app
"""
from sqlalchemy import * 
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, mapper
from sqlite3 import * 
from flask import Flask, render_template, request
# declaring app
app = Flask(__name__)
        


def main():
    
    # config db
    engine = create_engine('sqlite:///data.db')
    metadata = MetaData()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()
    # we declare the DB here because why be *there* when we can be *here* (python was whining)
    class Person(Base):
        __tablename__ = 'names'
        id = Column(Integer, primary_key= True)
        name = Column(String(50), unique=True)
        def __init__(self,name = None):
                self.name = name
    # this line of code feels like plugging in a 3-pronged charger with no ground
    Base.metadata.create_all(bind=engine)
    
    # app routing goes here until it causes issues
    @app.route('/')
    def form():
        return render_template('index.html') # I did the webpage in html, was I supposed to? IDK
    
    # get text when user enters it and store it in the DB
    @app.route('/', methods=["POST"])
    def on_name_entered():
        text = request.form['text']
        # if text is not empty, add it to the DB
        if text:
            new_person = Person(text)
            db_session.add(new_person)
            try:
                db_session.commit()
                return "You have successfully entered your name, was it recieved properly? idk"
            except(Exception):
                return repr(Exception)

# idk about my other practices but I think this one is good
if __name__ == "__main__":
    main()
    # we run this seperately so I don't get a headache
    app.run()