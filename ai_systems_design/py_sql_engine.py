class SQLEngine:
    def __init__(self, db_name="example.db"):
        self.db_name = db_name
        self._conn = None 
        self._cursor = None 
        self._closed = False 

    def _create_connection(self):
        """Simulate database creation"""
        self._conn = {
            'file': self.db_name,
            'cursor': {
                'execute': lambda stmt: None,
                'fetchone': lambda: None,
                'fetchall': lambda: []
            },
            'closed': False
        }

    def _open_connection(self):
        """Open connection to database"""
        self._create_connection()
        self._conn['cursor']['execute'] = lambda stmt: None,
        self._conn['cursor']['fetchone'] = lambda: None,
        self._conn['cursor']['fetchall'] = lambda: []

    def _close_connection(self):
        """Close the connection"""
        self._conn['closed'] = True 

    def execute(self, sql, params=None):
        """Execute an SQL Statement"""
        if not self._conn['closed']:
            self._conn['cursor']['execute'](sql)
            if params: 
                self._conn['cursor']['execute'](f'{'?'.join(['%s' for _ in params])}' % params)
        return self 
    
    def fetchone(self):
        """Fetch single row."""
        #TODO continue implementing when parsing SQL with our tech stack
        return self._conn['cursor']['fetchone']()
    
    def fetchall(self):
        """Fetch all rows."""
        return self._conn['cursor']['fetchall']()
    
    def commit(self):
        """Commit the transaction"""
        self._conn['cursor']['execute']("COMMIT")


if __name__ == "__main__":
    engine = SQLEngine()

    engine.create_table("Table SQL")

    engine.insert_data("Table name", "data")

    engine.query("SQL query")