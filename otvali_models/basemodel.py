from otvali_models.base import session, logger

class BaseModel:
    def __init__(self):
        if logger is not None:
            self.logger = logger
        else:
            import logging
            self.logger = logging.getLogger(__name__)

    def commit(self):
        try:
            session.add(self)
        except:
            session.rollback()
            self.logger.exception("An error occurred while committing.")
        else:
            session.commit()
            self.logger.debug("Committed successfully.")
        return self

    def delete(self):
        try:
            session.delete(self)
        except:
            session.rollback()
            self.logger.exception("An error occurred while deleting.")
        else:
            session.commit()
            self.logger.debug("Deleted successfully.")
        return self
