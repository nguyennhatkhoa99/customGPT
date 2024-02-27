import json

class GoogleDriveFile:
    def __init__(self, id:str, name:str, mimeType:str) -> None:
        self.id = id
        self.name = name
        self.mimeType = mimeType

    def get_info(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)   