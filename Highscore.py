# Importing classes
import speler-naam
import os

class Highscore:

    # Initialisatie van de highscore klasse
    def __init__(self, bestandsnaam):
        self.bestandsnaam = bestandsnaam
        self.scores = self.laad_scores()

    # Methode om scores te laden vanuit een bestand
    def laad_scores(self):
        if not os.path.exists(self.bestandsnaam):
            return []
        with open(self.bestandsnaam, 'r') as bestand:
            regels = bestand.readlines()
            scores = [regel.strip().split(',') for regel in regels]
            return [(naam, int(score)) for naam, score in scores]

    # Methode om een nieuwe score toe te voegen
    def voeg_score_toe(self, naam, score):
        self.scores.append((naam, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        self.sla_scores_op()

    # Methode om scores op te slaan naar een bestand
    def sla_scores_op(self):
        with open(self.bestandsnaam, 'w') as bestand:
            for naam, score in self.scores:
                bestand.write(f"{naam},{score}\n")

    # Methode om de highscores weer te geven
    def toon_highscores(self):
        print("Highscores:")
        for naam, score in self.scores:
            print(f"{naam}: {score}")

spelerNaam = speler.SpelerNaam(input("wat is jou naam: "))
speler = spelerNaam.get_naam()

highscore = Highscore('highscores.json')

def score(moelijkheid, maxPogingen, Pogingen):
    pass