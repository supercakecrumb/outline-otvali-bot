from models import session


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