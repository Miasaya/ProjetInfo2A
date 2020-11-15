from app.features.users.guest import Guest
from app.features.DAO.playerDAO import PlayerDAO
from app.features.users.playerView import PlayerView
from app.features.DAO.gameDAO import GameDAO
from app.features.game.gameMechanics.belote import Belote
from app.menus.menu_interface import MenuInterface

import hashlib


class Player(Guest):

    def __init__(self, identifiant=None, handList=[]):
        super().__init__(identifiant, handList)
        self.userType = 'Player'

    def changePassword():
        """ Changer le mot de passe d'un utilisateur """
        (motdepasse, new_mdp) = PlayerView.displayChangePassword()

        newhash_mdp = hashlib.sha256(new_mdp.encode()).hexdigest()
        hash_mdp = hashlib.sha256(motdepasse.encode()).hexdigest()
        # laisser faire la classe playerDAO
        PlayerDAO.updatePassword(hash_mdp, newhash_mdp)

    def seeScores():
        """Affiche les scores en appellant la fonction correspondante dans la DAO"""
        return(PlayerDAO.getAccountData())


class GameService:

    def __init__(self):
        pass

    @staticmethod
    def startGame(nomJeu, idJeu, PlayerGroup):
        if nomJeu == 'Belote':
            return(Belote(idJeu, PlayerGroup, False).gameLoop(idJeu, PlayerGroup))

    @staticmethod
    def initListPlayers(jeu):
        listPlayers = []
        if jeu == 'Belote':
            while not Belote.checkPlayerNumber(listPlayers):
                listPlayers = Guest.connexionJeu(listPlayers)
        return(listPlayers)

    @staticmethod
    def initEmptyGame(nomJeu, previous_menu):
        """initialise un jeu vide du jeu sélectionné avec une liste de joueur complete """
        listPlayers = GameService.initListPlayers(nomJeu)
        listString = ' '.join(map(str, listPlayers))
        # Convertit la liste de joueur [1,2,3] en string '1 2 3'
        id_Jeu = GameDAO.addGame(nomJeu, listString)
        players = []
        for i in listPlayers:
            players.append(Player(i))
        GameService.startGame(nomJeu, id_Jeu, players)
        return MenuInterface(previous_menu)
