#models/user.py

class User:
    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
    
    #getters and setters
    #nome
    
    @property
    def get_name(self):
        return self.name

    @get_name.setter   
    def set_name(self, name):   
        self.name = name
    
    @property
    def get_email(self):
        return self.email
    
    @get_email.setter
    def set_email(self, email):
        self.email = email

    @property
    def get_password(self):
        return self.password    
    
    @get_password.setter
    def set_password(self, password):
        self._password = password    
        