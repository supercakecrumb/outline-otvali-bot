from loggerconfig import getLogger
logger = getLogger(__name__)

from models import session

from datetime import datetime

class Model(): 
    
    def commit(self):
        try:
            session.add(self)
        except:
            session.rollback()
        else:
            session.commit()
        return self

    def delete(self):
        try:
            session.delete(self)
        except:
            session.rollback()
        else:
            session.commit()
        return self