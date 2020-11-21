
from app.features.users.guest import Guest
from app.security.id import verif_init_id
from app.features.DAO.playerDAO import PlayerDAO
from app.features.users.playerView import PlayerView
from app.features.users.guestView import GuestView
from app.features.DAO.gameDAO import GameDAO
from app.features.game.gameMechanics.belote import Belote
from app.menus.menu_interface import MenuInterface
from app.features.game.cardObjects.handPile import Hand, Pile

import hashlib


class Player(Guest):
    """ Classe Player qui regroupe les fonctionalités propres aux 
        utilisateurs possédant un compte
    """

    def __init__(self, identifiant=None, handList=[]):
        super().__init__(identifiant, handList)
        self.userType = 'Player'

    @staticmethod
    def changePassword(previous_menu):
        """ Permet de changer le mot de passe d'un utilisateur """
        (username, motdepasse, new_mdp) = PlayerView.displayChangePassword()

        newhash_mdp = hashlib.sha256(new_mdp.encode()).hexdigest()
        hash_mdp = hashlib.sha256(motdepasse.encode()).hexdigest()
        user = PlayerDAO.updatePassword(username, hash_mdp, newhash_mdp)
        input("Le mot de passe de " + str(user) + " a été modifié ")
        return MenuInterface(previous_menu)

    @staticmethod
    def changeUsername(previous_menu):
        """ Permet de changer le mot de passe d'un utilisateur """
        (username, motdepasse, new_name) = PlayerView.displayChangeName()
        while not verif_init_id(username):
            username = GuestView.displayVerifId()

        hash_mdp = hashlib.sha256(motdepasse.encode()).hexdigest()
        user = PlayerDAO.updateName(username, hash_mdp, new_name)
        input("Le pseudo de " + str(user) + " a été modifié ")
        return MenuInterface(previous_menu)

    def seeScores():
        """Affiche les scores en appellant la fonction correspondante dans la DAO"""
        return(PlayerDAO.getAccountData())


class GameService:
    """ Classe regroupant les différentes fonctions permettant l'initialisation
        d'une partie de jeu
    """

    def __init__(self):
        pass

    @staticmethod
    def startGame(nomJeu, idJeu, PlayerGroup):
        """ Lance une partie de jeu avec le groupe de joueur et l'identifiant du jeu """
        # TODO : Implémenter ici la reprise du jeu
        if nomJeu == 'Belote':
            return(Belote(idJeu, PlayerGroup, False).gameLoop(idJeu))

    @staticmethod
    def initListPlayers(jeu):
        """ Initialise la liste des joueurs participant aux jeu
        """
        listPlayers = []
        if jeu == 'Belote':
            while not Belote.checkPlayerNumber(listPlayers):
                listPlayers = Guest.connexionJeu(listPlayers)
        return(listPlayers)

    @staticmethod
    def initEmptyGame(nomJeu, previous_menu):
        """ Initialise un jeu vide du jeu sélectionné avec une liste de joueur complete """
        listPlayers = GameService.initListPlayers(nomJeu)
        listString = ' '.join(map(str, listPlayers))
        # Convertit la liste de joueur [1,2,3] en string '1 2 3'
        id_Jeu = GameDAO.addGame(nomJeu, listString)
        players = []
        for i in listPlayers:
            players.append(Player(i))
        GameService.startGame(nomJeu, id_Jeu, players)
        return MenuInterface(previous_menu)

    def getBackGame(self, idGame, nomJeu):
        data = GameDAO.getBackGame(idGame, nomJeu)
        if nomJeu == 'Belote':
            team1ID = data['players'].split()[0:1]
            team2ID = data['players'].split()[2:3]
            score1 = data['score1']
            score2 = data['score2']
            maitre = data['maitre']
            atout = data['atout']
            pointPlis = data['scorepliencours']
            team1 = [Player(team1ID[0]), Player(team1ID[0])]
            team2 = [Player(team2ID[0]), Player(team2ID[0])]

            for player in team1 + team2:
                player.handList = Hand.getHand(idGame, player.identifiant)

            return(Belote(idGame, team1+team2, False, team1, team2, score1, score2).gameLoop(idGame, maitre, atout,pointPlis))
