import logging
from sqlalchemy import create_engine

class MySQLReader(object):
    """Corpus reader for texts stored in MySQL database.
    
    This corpus reader provides a simple interface for iterating over texts
    or other information stored in a MySQL database. It returns named tuples
    (or more precisely: `sqlalchemy`'s `RowProxy` objects) for the result from
    a SQL query.
    """
    def __init__(self, user, passwd, host, database, query):
        """ Setup database connection.
        
        Parameters
        ----------
        
        user : string
            Database user for authentication.
            
        passwd : string
            Password for authenticating the user.
        
        host : string
            Hostname where the database server is running.
        
        database : string
            Name of the database to connect to.
        
        query : string
            Query to execute. This reader object will iterate over the result
            rows from this query.
        """
        self.logger = logging.getLogger('MySQLReader')
        self._query = query

        # establish database connection
        connection_string = 'mysql://{user:s}:{passwd:s}@{host:s}/{db:s}'.format(user = user,
                                                                                 passwd = passwd,
                                                                                 host = host,
                                                                                 db = database)
        self.logger.debug("using DB connection string '%s'", connection_string)
        try:
            self.engine = create_engine(connection_string)
        except:
            self.logger.critical('failed to establish DB connection')
            raise
        else:
            self.logger.info("established connection to DB '%s' with user '%s'", database, user)
    
    def __iter__(self):
        """Result iterator.
        
        Returns
        -------
        
        result : generator
            Generator over result rows which are named tuples.
        """
        yield from self.engine.execute(self._query).fetchall()
    
    def head(self, n = 5):
        """Show example data.
        
        This function returns the `n` first result rows.
        
        Parameters
        ----------
        
        n : int, Default = 5
            Number of rows to return
            
        Returns
        -------
        
        rows : list
            List of named tuples for the first `n` result rows.
        """
        result = []
        it = iter(self)
        for _ in range(n):
            try:
                result.append(next(it))
            except StopIteration:
                break
        return result
