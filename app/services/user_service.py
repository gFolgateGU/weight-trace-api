from app.models.models import User
from app import application

class UserService:
    def __init__(self):
        pass

    def create_user(self, strava_id, username):
        new_user = None
        session = None
        try:
            # Start a new session
            session = application.db()
            
            # Create a new user instance
            new_user = User(strava_id=strava_id, username=username)

            # Check if a user exists
            existing_user = session.query(User).filter((User.username == new_user.username)).first()
            if existing_user:
                return new_user

            # Add the user to the session
            session.add(new_user)
            
            # Commit the transaction
            session.commit()
            
        except Exception as error:
            # Roll back the transaction in case of an error
            if session:
                session.rollback()
            print(f"Error: {error}")
        finally:
            # Close the session
            if session:
                session.close()
        
        return new_user
        