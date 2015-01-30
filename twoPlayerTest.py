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
        
        self.addDeck = QPushButton('Add a deck')
        self.addDeck.clicked.connect(lambda: self.addYourDeck())
        grid = QGridLayout()
        grid.addWidget(self.myDeckLabel, 0, 0)
        grid.addWidget(self.opponent, 1, 0)
        grid.addWidget(self.deckList, 1, 1)
        grid.addWidget(self.button,2,0)
        grid.addWidget(self.addDeck,4,1)

        self.setLayout(grid)

        self.button.clicked.connect(lambda: self.nextStep())
    def updateUi(self):
        to = self.opponent.currentText()
        from_ = self.deckList.currentText()

    def nextStep(self):
    	nextStep = ShowDecks(self.opponent.currentText(),self.decks[self.deckList.currentText()]) 
        if nextStep.exec_():
        	print ''
        else:
            QMessageBox.warning(self, 'lolol', "next round")
    def getDecks(self):
        decks = {} 
        decks['warlock']  = {'defender of arguts':2,'power overwhelming':1, 'abusive sergent':2,'flame imp':2 , 'undertaker':2,'leper gnome':2,'voidwalker':2,'dire wolf alpha':2,'echoing ooze':2,'haunted creeper':2,'knife juggler':2,'nerubian egg':2,'harvest golem':2,'imp-losion':2,'dark iron dwarfs':1,'doomgaurd':2,'sea giant':1}
        decks['taco mage'] = {'dragon':2,'flame strike':1}
        return decks
    def heros(self):
        listOfHeros = ['warlock', 'mage','hunter','rouge','shaman','paladin','priest','druid','warrior']
        return listOfHeros
    def addYourDeck(self): 
        print 'lol'	
class ShowDecks(QDialog) : 
    def __init__(self,opp,deck, parent=None):
        super(ShowDecks, self).__init__(parent)
        self.grid = QGridLayout()
        self.qLabelName = [QLabel(i) for i in deck.keys()]
        self.titleNCards = QLabel('number of cards left')
        self.grid.addWidget(self.titleNCards,0,5)
        self.titleName = QLabel('name of card')
        self.grid.addWidget(self.titleName,0,4)
        self.titleProb = QLabel('prob to get card')
        self.grid.addWidget(self.titleProb,0,8)
        self.titleCardPlayed = QLabel('This card was drawn')
        self.grid.addWidget(self.titleCardPlayed,0,7)
        self.titleWrong = QLabel('pressed wrong button')
        self.grid.addWidget(self.titleWrong,0,6)
        
        k = 1 
        for i in self.qLabelName : 
            self.grid.addWidget(i,k,4)
            k = k + 1 

        self.qAddButton = [QPushButton('+') for i in deck.keys()]
        self.qSubtractButton = [QPushButton('-') for i in deck.keys()]
        self.qLabelVal = [QLabel('') for i in deck.keys()] 
        k = 1 
        for i in self.qLabelVal : 
            key = sorted(deck.keys())
            i.setText(str(deck[key[k-1]]))
            self.grid.addWidget(self.qSubtractButton[k-1],k,6)
            self.grid.addWidget(i,k,5)
            self.grid.addWidget(self.qAddButton[k-1],k,7)
            k = k + 1 
        k = 1
        [i.setDefault(False) for i in self.qSubtractButton]
        [i.setDefault(False) for i in self.qAddButton]

        self.totCards = 30.
        self.qLabelPercent = [QLabel('') for i in deck.keys()]
        for i in self.qLabelPercent : 
            key = sorted(deck.keys())
            val = str(deck[key[k-1]]/self.totCards)
            i.setText(val)
            self.grid.addWidget(i,k,8)
            k = k + 1 
        self.qLabelCoin = QCheckBox('coin played?')
        self.grid.addWidget(self.qLabelCoin,k,0)
        self.connect1 = [self.qAddButton[i].clicked.connect(lambda i=i: self.valChangeAdd(self.qLabelVal[i],i)) for i in range(len(self.qLabelVal))]
        self.connect2 = [self.qSubtractButton[i].clicked.connect(lambda i=i: self.valChangeSub(self.qLabelVal[i],i)) for i in range(len(self.qLabelVal))]            
        self.deckList = {'druid':'druidList.txt', 'huntard':'huntardList.txt', 'mage' :'mageList.txt', 'paladin':'paladinList.txt', 'priest':'priestList.txt', 'rogue':'rogueList.txt', 'shaman':'shamanList.txt',  'warlock':'warlock.txt', 'warrior' :'warriorList.txt'}
        oppCards = self.getCards(self.deckList[opp])
        self.nCards = 0
        self.lineEdit = QLineEdit(self)
        self.completer = QCompleter(oppCards, self)
        self.lineEdit.setCompleter(self.completer)      
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.grid.addWidget(self.lineEdit,0,0) 
        self.grid.addWidget(QLabel('name of card'),0,1)
        self.grid.addWidget(QLabel('number of times played'),0,2)
        self.lineEdit.returnPressed.connect(lambda : self.addCard(self.lineEdit.text(),oppCards))
        self.labels = []
        self.counters = []
        self.removeButtons = []        
        self.setLayout(self.grid)
    def valChangeAdd(self,target,btnNumb):
        val = int(target.text())
        self.qAddButton[btnNumb].setDefault(False)
        target.setText(str(val - 1))
        self.totCards = self.totCards - 1 
        self.changeProb() 
    def valChangeSub(self,target,btnNumb):
        val = int(target.text())
        target.setText(str(val + 1))
        self.qSubtractButton[btnNumb].setDefault(False)
        self.totCards = self.totCards + 1 
        self.changeProb()
    def changeProb(self):   
        for i in range(len(self.qLabelPercent)) : 
            nCard = self.qLabelVal[i].text()
            val = str(int(nCard)/self.totCards)
            self.qLabelPercent[i].setText(val) 
        print self.totCards
    def addCard(self,cardName,cardDeck):
        notInDeck = True
        if cardName not in cardDeck:
            return 
        if self.nCards > 0 :
            for i in range(self.nCards):
                if cardName == self.labels[i].text():
                    self.counters[i].setText(str(int(self.counters[i].text())+1))
                    notInDeck = False
        if notInDeck : 
            nCard = self.nCards 
            self.labels.append(QLabel(cardName))
            self.counters.append(QLabel('1'))
            self.removeButtons.append(QPushButton('remove'))
            self.removeButtons[-1].setCheckable(True)
            self.grid.addWidget(self.labels[self.nCards],self.nCards+1,1)
            self.grid.addWidget(self.counters[self.nCards],self.nCards+1,2)
            self.grid.addWidget(self.removeButtons[self.nCards],self.nCards+1,3)
            self.removeButtons[self.nCards].clicked.connect(lambda: self.removeCard(nCard)) 
            self.nCards = self.nCards+1
            self.setLayout(self.grid)
    def removeCard(self,cardName): 
        if int(self.counters[cardName].text()) > 0 : 
            self.counters[cardName].setText(str(int(self.counters[cardName].text()) - 1 ))
            self.removeButtons[cardName].setDefault(False)
    def getCards(self,deck):
        with open('cards/neutralList.txt') as f:
            content = f.readlines()
        neutralCards = [i.replace('\n','').replace('GVGIcon','').replace('CurseofNaxxramasLogo','') for i in content]
        with open('cards/'+ deck) as f:
            content = f.readlines()
        classDependentCards = [i.replace('\n','').replace('GVGIcon','').replace('CurseofNaxxramasLogo','') for i in content]
        neutralCards = neutralCards + classDependentCards
        return neutralCards     

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()