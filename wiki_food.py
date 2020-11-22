
class WikiFood:
    ''' An object for storing food metadata scraped from Wikipedia'''

    def __init__(self, name, description, image_src):
        print('-- ', name, "|", description, "|", image_src)
        self.name = name.replace('"', "'")
        self.description = description.replace('"', "'")
        self.image_src = image_src

    def __str__(self):
        return f'- {self.name} - {self.description} ({self.image_src})'

    def insert_cmd(self):
        return f'''
        INSERT INTO Foods VALUES( NULL, "{self.name}", "{self.description}", "{self.image_src}" );
      '''
