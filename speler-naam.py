# Class voor speler naam
class SpelerNaam:
    def __init__(self, naam):
        self.naam = naam
    def get_naam(self):
        return self.naam

# Voorbeeld van gebruik
naamInput = input("Voer de naam van de speler in: ")
spelerNaam = SpelerNaam(naamInput)

print("De naam van de speler is:", spelerNaam.get_naam())
