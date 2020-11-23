
from app.features.users.guest import Guest
from app.security.id import verif_init_id
from app.features.DAO.playerDAO import PlayerDAO
from app.features.users.playerView import PlayerView
from app.features.users.guestView import GuestView
from app.features.DAO.gameDAO import GameDAO
from app.features.game.gameMechanics.belote import Belote
from app.menus.menu_interface import MenuInterface
from app.features.game.cardObjects.handPile import Hand
from app.features.utils import rotate

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

    @staticmethod
    def seeScoresBelote(previous_menu):
        """Affiche les scores en appellant la fonction correspondante dans la DAO"""
        id_users = Guest.connexion()
        scores = PlayerDAO.getAccountDataBelote(id_users)
        if len(scores) == 0:
            input("Aucune partie trouvée ")
        else:
            print("Vos précédentes parties sont : ")
            for score in scores:
                print(score)
        input("Affichage terminé ")
        return MenuInterface(previous_menu)


class GameService:
    """ Classe regroupant les différentes fonctions permettant l'initialisation
        d'une partie de jeu
    """

    def __init__(self):
        pass

    @staticmethod
    def startGame(nomJeu, idJeu, PlayerGroup, saved):
        """ Lance une partie de jeu avec le groupe de joueur et l'identifiant du jeu """
        # TODO : Implémenter ici la reprise du jeu
        if nomJeu == 'Belote':
            return(Belote(idJeu, PlayerGroup, False, save=saved).gameLoop(idJeu))

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
        saved = True
        for player in listPlayers:
            if "invité" in player:
                saved = False
                break
        listString = ' '.join(map(str, listPlayers))
        # Convertit la liste de joueur [1,2,3] en string '1 2 3'
        id_Jeu = GameDAO.addGame(nomJeu, listString)
        players = []
        for i in listPlayers:
            players.append(Player(i))
        GameService.startGame(nomJeu, id_Jeu[0][0], players, saved)
        return MenuInterface(previous_menu)

    @staticmethod
    def initPreviousGame(nomJeu, previous_menu):
        """ Initialise un jeu vide du jeu sélectionné avec une liste de joueur complete """
        listPlayers = GameService.initListPlayers(nomJeu)
        for i in range(len(listPlayers)):
            listString = ' '.join(map(str, listPlayers))
            listPlayers = rotate(listPlayers)
            # Convertit la liste de joueur [1,2,3] en string '1 2 3'
            id_Jeu = GameDAO.getIDwithPlayers(listString, nomJeu)
            if id_Jeu is not None:
                GameService.getBackGame(id_Jeu, nomJeu)
                break
            else:
                input("Aucune partie n'a été trouvée, " +
                      str(len(listPlayers)-i)+" tentatives restantes ")
        return MenuInterface(previous_menu)

    @staticmethod
    def getBackGame(idGame, nomJeu):
        data = GameDAO.getBackGame(idGame, nomJeu)
        if nomJeu == 'Belote':
            team1ID = data[1].split()[0:2]
            team2ID = data[1].split()[2:4]
            score1 = data[3]
            score2 = data[4]
            maitre = data[6]
            atout = data[5]
            team1 = [Player(team1ID[0]), Player(team1ID[0])]
            team2 = [Player(team2ID[0]), Player(team2ID[0])]

            for player in team1 + team2:
                player.handList = Hand.getHand(idGame, player.identifiant)

            return(Belote(idGame, team1+team2, False, team1, team2, score1, score2, True).gameLoop(idGame, maitre, atout))
