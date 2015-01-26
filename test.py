import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.decks = self.getDecks()
        nameOfDecks = sorted(self.decks.keys())
        self.nameOfHeros = self.heros()
        nameOfHeros = sorted(self.nameOfHeros)

        self.deckList = QComboBox()
        self.deckList.setItemText(0,'choose your deck')     
        self.deckList.addItems(nameOfDecks)  
        self.button = QPushButton("continue")

        self.myDeckLabel = QLabel('choose carefully')

        self.opponent = QComboBox()
        self.opponent.setItemText(0,'choose your opponent')
        self.opponent.addItems(nameOfHeros)       
        
        self.testLabel1 = QLabel('tester1')
        self.testLabel2 = QLabel('teste2')
        grid = QGridLayout()
        grid.addWidget(self.myDeckLabel, 0, 0)
        grid.addWidget(self.opponent, 1, 0)
        grid.addWidget(self.deckList, 1, 1)
        grid.addWidget(self.button,2,0)
        grid.addWidget(self.testLabel1, 3, 0)
        grid.addWidget(self.testLabel2,3,1)
        

        self.setLayout(grid)

        self.connect(self.opponent, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.deckList, SIGNAL("currentIndexChanged(int)"), self.updateUi)
        self.connect(self.button,SIGNAL("clicked()"),self.nextStep)
    def updateUi(self):
        to = self.opponent.currentText()
        from_ = self.deckList.currentText()
        self.testLabel1.setText(to)
        self.testLabel2.setText(from_)

    def nextStep(self):
    	nextStep = ShowDecks(self.opponent.currentText(),self.decks[self.deckList.currentText()]) 
        if nextStep.exec_():
        	print 'bajs'
        else:
            QMessageBox.warning(self, 'lolol', "next round")
    def getDecks(self):
        decks = {} 
        decks['warlock']  = {'power overwhelming':1, 'abusive sergent':2,'flame imp':2 , 'undertaker':2,'leper gnome':2,'voidwalker':2,'dire wolf alpha':2,'echoing ooze':2,'haunted creeper':2,'knife juggler':2,'nerubian egg':2,'harvest golem':2,'imp-losion':2,'dark iron dwarfs':1,'doomgaurd':2,'sea giant':1}
        decks['taco mage'] = {'dragon':2,'flame strike':1}
        return decks
    def heros(self):
        listOfHeros = ['warlock', 'mage','hunter','rouge','shaman','paladin','priest','druid','warrior']
        return listOfHeros
	
class ShowDecks(QDialog) : 
    def __init__(self,opp,deck, parent=None):
        super(ShowDecks, self).__init__(parent)
        grid = QGridLayout()
        self.qLabelName = [QLabel(i) for i in deck.keys()]
        self.titleNCards = QLabel('number of cards left')
        grid.addWidget(self.titleNCards,0,4)
        self.titleName = QLabel('name of card')
        grid.addWidget(self.titleName,0,3)
        self.titleProb = QLabel('prob to get card')
        grid.addWidget(self.titleProb,0,7)
        self.titleCardPlayed = QLabel('Card Played')
        grid.addWidget(self.titleCardPlayed,0,6)
        self.titleWrong = QLabel('wrong button')
        grid.addWidget(self.titleWrong,0,5)
        
        k = 1 
        for i in self.qLabelName : 
            grid.addWidget(i,k,3)
            k = k + 1 

        self.qAddButton = [QPushButton('+') for i in deck.keys()]
        self.qSubtractButton = [QPushButton('-') for i in deck.keys()]
        self.qLabelVal = [QLabel('') for i in deck.keys()] 
        k = 1 
        for i in self.qLabelVal : 
            key = deck.keys()
            i.setText(str(deck[key[k-1]]))
            grid.addWidget(i,k,4)
            grid.addWidget(self.qSubtractButton[k-1],k,5)
            grid.addWidget(self.qAddButton[k-1],k,6)
            k = k + 1 
        k = 1
        self.totCards = 30.
        self.qLabelPercent = [QLabel('') for i in deck.keys()]
        for i in self.qLabelPercent : 
            key = deck.keys()
            val = str(deck[key[k-1]]/self.totCards)
            i.setText(val)
            grid.addWidget(i,k,7)
            k = k + 1 
        self.qLabelCoin = QCheckBox('coin played?')
        grid.addWidget(self.qLabelCoin,k,0)
        self.connect1 = [self.qAddButton[i].clicked.connect(lambda i=i: self.valChangeAdd(self.qLabelVal[i])) for i in range(len(self.qLabelVal))]
        self.connect2 = [self.qSubtractButton[i].clicked.connect(lambda i=i: self.valChangeSub(self.qLabelVal[i])) for i in range(len(self.qLabelVal))]            
        self.setLayout(grid)
    def valChangeAdd(self,target):
        val = int(target.text())
        target.setText(str(val - 1))
        self.totCards = self.totCards - 1 
        self.changeProb() 
    def valChangeSub(self,target):
        val = int(target.text())
        target.setText(str(val + 1))
        self.totCards = self.totCards + 1 
        self.changeProb()
    def changeProb(self):   

        for i in range(len(self.qLabelPercent)) : 
            nCard = self.qLabelVal[i].text()
            val = str(int(nCard)/self.totCards)
            self.qLabelPercent[i].setText(val) 
        print self.totCards
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()