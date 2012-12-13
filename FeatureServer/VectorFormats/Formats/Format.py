class Format(object):
    """Base Format class. To set properties on your subclasses, you can
       pass them as kwargs to your format constructor."""
    def __init__(self, service, *args, **kwargs):
        self._service = service
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def escapeSQL(self, value):
        newValue = value
        newValue = value.replace("'", "''")
        
        return newValue 

    @property
    def service(self):
        return self._service