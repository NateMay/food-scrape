class WikiCategory:
    ''' An object for storing food categories scraped from Wikipedia'''

    def __init__(self, name, description, foods, parent=None):
        self.name = name.replace('"', "'")
        self.description = description.replace('"', "'")
        self.foods = foods
        self.parent = parent

    def __str__(self):
        return f'{self.parent} : {self.name} - {self.description}'

    def insert_cmd(self):
        return f'''
        INSERT INTO Categories VALUES( NULL, "{self.name}", "{self.description}", "{self.parent}" );
      '''
      

OTHER_CATEGORIES = {
    'poultry': ['Cassowary', 'Chicken', 'Duck', 'Emu', 'Goose', 'Grouse', 'Ostrich', 'Partridge', 'Pheasant', 'Pigeon', 'Quail', 'Rhea', 'Turkey'],
    'livestock': ['Alpaca', 'Beef', 'Beefalo', 'Bison', 'Buffalo', 'Camel', 'Cat', 'Chevon (goat meat)', 'Dog', 'Elephant', 'Escargot', 'Frog', 'Cat', 'Guinea pig (Cuy)', 'Horse', 'Lamb and mutton', 'Llama', 'Pork', 'Veal', 'Yak', 'Żubroń'],
    'game': ['Alligator', 'Bat', 'Bear', 'Crocodile', 'Kangaroo', 'Monkey', 'Pangolin', 'Rat', 'Hare and rabbit', 'Snake', 'Turtle', 'Venison', 'Wolf'],
    'fish': ['Anchovy', 'Basa', 'Bass', 'Carp', 'Catfish', 'Cod', 'Crappie', 'Eel', 'Flounder', 'Grouper', 'Haddock', 'Halibut', 'Herring', 'Kingfish', 'Mackerel', 'Mahi Mahi', 'Marlin', 'Milkfish', 'Orange roughy', 'Pacific saury', 'Perch', 'Pike', 'Pollock', 'Salmon', 'Sardine', 'Shark', 'Sole', 'Swai', 'Swordfish', 'Tilapia', 'Trout', 'Tuna', 'Walleye'],
    'seafood': ['Abalone', 'Calamari', 'Clams', 'Crab', 'Crayfish', 'Dolphin', 'Lobster', 'Mussel', 'Octopus', 'Oyster', 'Scallop', 'Seal meat', 'Shrimp/prawn', 'Sea urchin', 'Whale']
}
