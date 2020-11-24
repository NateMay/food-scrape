class WikiCategory:
    ''' An object for storing food categories scraped from Wikipedia'''

    def __init__(self, name, description, foods, parent=None):
        self.name = name
        self.description = description
        self.foods = foods
        self.parent = parent
        print(self)

    def __str__(self):
        return f'CATEGORY: {self.parent} > {self.name} : {self.description[:40]}... {len(self.foods)} foods. \n'

    def insert_cmd(self):
        return (
            "INSERT INTO Categories VALUES(NULL, ?, ?, ?)",
            (self.name, self.description, self.parent)
        )


class WikiFood:
    ''' An object for storing food metadata scraped from Wikipedia'''

    def __init__(self, name, description, image_src):
        self.name = name
        self.description = description
        self.image_src = image_src
        print(self)

    def __str__(self):
        return f'- {self.name} - {self.description[:40]}... \n'

    def insert_cmd(self, categories):
        return (
            "INSERT INTO Foods VALUES(NULL, ?, ?, ?, ?, ?)",
            (self.name, self.description, self.image_src,
             categories[0], categories[1])
        )


def populate_dummies():
    return [WikiCategory('Category Name', 'Category Description', [
        WikiFood('A food', 'A description', 'An image')
    ], 'Parent Category')]

# 
