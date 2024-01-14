# inizializzazione di customtkinter con i suoi settings di default
import customtkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# inizializzazione degli strumenti che verranno utilizzati all'interno del programma
import Tools as tools
import random as generate
import pygame as audioPlayer # pygame viene inizializzato con questo nome perché verrà usato solo per riprodurre audio







# CODE-SECT: scelta della difficoltà
def changeDifficulty(chosenDifficulty):
    #? funzione che cambia variabile della difficoltà
    
    global difficulty
    difficulty = chosenDifficulty



# separatore



def difficultySelection():
    #? funzione di scelta della difficoltà tramite GUI

    global difficultySelection_Window

    #* inizializzazione della finestra di selezione della difficoltà
    difficultySelection_Window = customtkinter.CTk()
    difficultySelection_Window.geometry( "600x400" )                    # definizione delle dimensioni
    difficultySelection_Window.resizable( width=False , height=False )  # viene impedito all'utente di cambiare le dimensioni della finestra
    difficultySelection_Window.title( "Battleship" )                    # viene definito il titolo della finestra

    difficultySelection_Window.iconbitmap( "Battleship.ico" )           # viene utilizzato il file "Battleship.ico" come icona del software



    #* inizializzazione di un frame per ragioni estetiche
    difficulySelection_Window_beautyFrame = customtkinter.CTkFrame ( master=difficultySelection_Window )
    difficulySelection_Window_beautyFrame.pack( pady=20 , padx=60 , fill="both" , expand=True )



    #* inizializzazione di un Label che comunicherà all'utente la funzione della finestra visualizzata
    difficultySelection_Window_communicationLabel = customtkinter.CTkLabel( master=difficulySelection_Window_beautyFrame , text="Choose the game's difficulty" , font=( "Berlin Sans FB" , 36 ) )
    difficultySelection_Window_communicationLabel.pack( pady=12 , padx=10 )



    #* inizializzazione del menù a tendina che permetterà all'utente di scegliere la difficoltà del gioco
    chosenDifficulty = customtkinter.StringVar( value="Easy" )
    difficultySelection_Window_comboBox = customtkinter.CTkComboBox( master=difficulySelection_Window_beautyFrame , \
                                                                     values=["Easy" , "Medium" , "Hard" , "Hell" ] , \
                                                                     command=changeDifficulty , \
                                                                     variable=chosenDifficulty)
    difficultySelection_Window_comboBox.pack( pady=10 , padx=20 )



    #* inizializzazione del pulsante che conferma la scelta della difficoltà
    difficultySelection_Window_confirmChoiceButton = customtkinter.CTkButton( master=difficulySelection_Window_beautyFrame , text="GO" , font=( "Berlin Sans FB " , 24 , "bold" ) , \
                                                                              command=difficultySelection_Window.destroy )
    difficultySelection_Window_confirmChoiceButton.pack( pady=12 , padx=10 )



    #* inizializzazione del pulsante che permette all'utente di cambiare il "tema" a scuro
    changeThemeToLight_button = customtkinter.CTkButton( master=difficulySelection_Window_beautyFrame , text="Light Theme" , font=( "Berlin Sans FB" , 18 ) , \
                                                         command=lambda: customtkinter.set_appearance_mode( "light" ) , fg_color="gray" , text_color="white" )
    changeThemeToLight_button.pack( pady=12 , padx=10 )

    #* inizializzazione del pulsante che permette all'utente di cambiare il "tema" a scuro
    changeThemeToDark_button = customtkinter.CTkButton( master=difficulySelection_Window_beautyFrame , text="Dark Theme" , font=( "Berlin Sans FB" , 18 ) , \
                                                       command=lambda: customtkinter.set_appearance_mode( "dark" ) , fg_color="#151515" , text_color="white" )
    changeThemeToDark_button.pack( pady=12 , padx=10 )



    difficultySelection_Window.protocol( "WM_DELETE_WINDOW" , exit ) 
    difficultySelection_Window.mainloop()






# CODE-SECT: posizionamento delle navi nella tabella dell'utente
def shipPlacement_confirm():
    #? funziona che conferma il posizionamento delle navi scelto e dà inizio al gioco
    
    audioPlayer.mixer.Sound( "./Sound Effects/Start-Game.wav" ).play() # riproduzione del suono di inizio gioco

    global userShipPlacementSelection_Window
    userShipPlacementSelection_Window.destroy()



# separatore



def drawTable():
    #? funzione che crea una griglia nella quale viene rappresentata la tabella dell'utente
    
    global userShipPlacementSelection_Window, userShipPlacementSelection_Window_beautyFrame

    #* inizializzazione del frame che conterrà la tabella
    global userShipPlacementSelection_Window_tableFrame
    userShipPlacementSelection_Window_tableFrame = customtkinter.CTkFrame( master=userShipPlacementSelection_Window_beautyFrame )
    userShipPlacementSelection_Window_tableFrame.pack( pady=20 , padx=60 )



    #* disegnamento della tabella (e dei riferimenti delle colonne e delle righe)
    global userShipPlacementSelection_Window_playerTable
    riferimentiColonne = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] # lo " " è utilizzato per dare la possibilità di posizionare anche i riferimenti per le righe
    riferimentiRighe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    for row in range(11):

        for column in range(11):
            if row == 0: # if che permette di scrivere il riferimento delle colonne
                cell = customtkinter.CTkLabel( master=userShipPlacementSelection_Window_tableFrame , width=25 , text=riferimentiColonne[column] , font=( "Berlin Sans FB" , 18 ) )
            
            elif column == 0: # if che permette di scrivere il riferimento delle righe
                cell = customtkinter.CTkLabel( master=userShipPlacementSelection_Window_tableFrame , width=25 , text=str( riferimentiRighe[row-1] ) , font=( "Berlin Sans FB" , 18 ) )

            else: # scrittura del contenuto di una determinata casella
                cell = customtkinter.CTkLabel( master=userShipPlacementSelection_Window_tableFrame , width=25 , text=userShipPlacementSelection_Window_playerTable[row-1][column-1] , \
                                               font=( "Berlin Sans FB" , 18 ) )

            cell.grid (row=row , column=column )



# separatore



def rerollPlacements():
    #? funzione che riposiziona le navi e re-inizializza alcuni elementi della finestra, che risulterebbero altrimenti cambiati di posizione
        # /!\ vengono distrutti anche i pulsanti in quanto la tabella risulterebbe cambiata di posto

    #* generazione della nuova tabella
    global userShipPlacementSelection_Window_playerTable
    userShipPlacementSelection_Window_playerTable = tools.randomPlaceShips( tools.initTabella() , difficulty )



    #* distruzione della tabella vecchia e rappresentazione della tabella nuova
    global userShipPlacementSelection_Window_tableFrame
    userShipPlacementSelection_Window_tableFrame.destroy()
    drawTable()



    #* distruzione dei pulsanti e inizializzazione di pulsanti nuovi
    global confirmShipPlacement_button
    confirmShipPlacement_button.destroy()

    global rerollShipPlacement_button
    rerollShipPlacement_button.destroy()

    placeButtons_shipPlacementWindow()



# separatore



def placeButtons_shipPlacementWindow():
    #? funzione che inizializza due pulsanti

    global userShipPlacement_Window, userShipPlacementSelection_Window_beautyFrame

    # queste variabili sono rese globali per renderne possibile la distruzione
    global confirmShipPlacement_button, rerollShipPlacement_button

    #* inizializzazione del pulsante che w
    confirmShipPlacement_button = customtkinter.CTkButton( master=userShipPlacementSelection_Window_beautyFrame , text="▶" , font=( "Berlin Sans FB " , 24, "bold" ) , command=shipPlacement_confirm )
    confirmShipPlacement_button.pack( pady=12 , padx=10 )



    #* inizializzazione del pulsante che genera una nuova tabella
    rerollShipPlacement_button = customtkinter.CTkButton( master=userShipPlacementSelection_Window_beautyFrame , text="↻" , fg_color="red" , font=( "Berlin Sans FB" , 24 ) , command=rerollPlacements )
    rerollShipPlacement_button.pack( pady=12 , padx=10 )



# separatore



def shipPlacementSelection():
    #? funzione di posizionamento delle navi dell'utente tramite GUI
    
    #* inizializzazione della finestra di selezione del posizionamento delle navi
    global userShipPlacementSelection_Window #? la variabile "userShipsWindow" è resa globale per facilitare le interazioni delle funzioni con essa

    userShipPlacementSelection_Window = customtkinter.CTk()
    userShipPlacementSelection_Window.geometry( "500x625" )                    # definizione delle dimensioni
    userShipPlacementSelection_Window.resizable( width=False , height=False )  # viene impedito all'utente di cambiare le dimensioni della finestra
    userShipPlacementSelection_Window.title( "Battleship" )                    # viene definito il titolo della finestra

    userShipPlacementSelection_Window.iconbitmap( "Battleship.ico" )           # viene utilizzato il file "Battleship.ico" come icona del software



    #* inizializzazione di un frame per ragioni estetiche
    global userShipPlacementSelection_Window_beautyFrame
    userShipPlacementSelection_Window_beautyFrame = customtkinter.CTkFrame( master=userShipPlacementSelection_Window )
    userShipPlacementSelection_Window_beautyFrame.pack( pady=12 , padx=10 )
    
    
    
    #* inizializzazione di un Label che comunicherà all'utente la funzione della finestra visualizzata
    global userShipPlacementSelection_Window_communicationLabel_windowFunction
    userShipPlacementSelection_Window_communicationLabel_windowFunction = customtkinter.CTkLabel( master=userShipPlacementSelection_Window_beautyFrame , \
                                                                                                  text="This is your table: press ↻ to reroll the ships' placement" , font=( "Berlin Sans FB" , 18 ) )
    userShipPlacementSelection_Window_communicationLabel_windowFunction.pack( pady=12 , padx=10 )



    #* inizializzazione di un label che spiega all'utente il significato dei simboli
    global userShipPlacementSelection_Window_communicationLabel_symbolsMeaning
    userShipPlacementSelection_Window_communicationLabel_symbolsMeaning = customtkinter.CTkLabel( master=userShipPlacementSelection_Window_beautyFrame , \
                                                                                                  text="~ = EMPTY SPACES;\nO = OCCUPIED SPACES" , font=( "Berlin Sans FB" , 18 ) )
    userShipPlacementSelection_Window_communicationLabel_symbolsMeaning.pack( pady=12 , padx=10 )



    #* disegnamento della tabella dell'utente
    drawTable()



    #* inizializzazione dei pulsanti di chisura della finestra (e quindi di gioco) e di generazione di una nuova tabella
    placeButtons_shipPlacementWindow()



    userShipPlacementSelection_Window.protocol( "WM_DELETE_WINDOW" , exit )
    userShipPlacementSelection_Window.mainloop()






# CODE-SECT: fase di gioco
def loseGame():
    #? funzione che chiude la finestra di gioco e comunica all'utente la sconfitta
    
    global playGame_Window
    playGame_Window.destroy()
    
    global finalWindow

    # riproduzione del suono che comunica all'utente la sconfitta
    if generate.randint(0, 1024) != 1024:
        audioPlayer.mixer.Sound( "./Sound Effects/Loss_Normal.wav" ).play()

    else:
        audioPlayer.mixer.Sound ( "./Sound Effects/Loss_Rare.wav" ).play() # easter-egg
    
    #* inizializzazione della finestra
    finalWindow = customtkinter.CTk()
    finalWindow.geometry( "450x300" )                     # definizione delle dimensioni
    finalWindow.resizable( width=False , height=False )   # viene impedito all'utente di cambiare le dimensioni della finestra
    finalWindow.title( "Battleship" )                     # viene definito il titolo della finestra
    finalWindow.iconbitmap( "Battleship.ico" )            # viene utilizzato il file "Battleship.ico" come icona del software



    #* inizializzazione di un frame per ragioni estetiche
    finalWindow_beautyFrame = customtkinter.CTkFrame( master=finalWindow )
    finalWindow_beautyFrame.pack( pady=20 , padx=60 , fill="both" , expand=True )



    #* inizializzazione di un label che comunica all'utente la sconfitta
    finalWindow_communicationLabel = customtkinter.CTkLabel( master=finalWindow_beautyFrame , text="YOU LOST!" , font=( "Berlin Sans FB" , 36 ) , text_color="white" )
    finalWindow_communicationLabel.pack( pady=12 , padx=10 , expand=True )



    #* inizializzazione di un pulsante che permette all'utente di cominciare a giocare di nuovo
    finalWindow_playAgainButton = customtkinter.CTkButton( master=finalWindow_beautyFrame , text="PLAY AGAIN" , font=( "Berlin Sans FB" , 18 ) , command=main )
    finalWindow_playAgainButton.pack( pady=12 , padx=10 , expand=True )



    finalWindow.mainloop()



# separatore



def winGame():
    #? funzione che chiude la finestra di gioco e comunica all'utente la vittoria
    
    global playGame_Window
    playGame_Window.destroy()
    
    global finalWindow

    audioPlayer.mixer.Sound( "./Sound Effects/Victory.wav" ).play()

    #* inizializzazione della finestra
    finalWindow = customtkinter.CTk()
    finalWindow.geometry( "450x300" )                       # definizione delle dimensioni
    finalWindow.resizable( width=False , height=False )     # viene impedito all'utente di cambiare le dimensioni della finestra
    finalWindow.title( "Battleship" )                       # viene definito il titolo della finestra
    finalWindow.iconbitmap("Battleship.ico")                # viene utilizzato il file "Battleship.ico" come icona del software



    #* inizializzazione di un frame per ragioni estetiche
    finalWindow_beautyFrame = customtkinter.CTkFrame( master=finalWindow )
    finalWindow_beautyFrame.pack( pady=20 , padx=60 , fill="both" , expand=True )



    #* inizializzazione di un label che comunica all'utente la vittoria
    finalWindow_communicationLabel = customtkinter.CTkLabel( master=finalWindow_beautyFrame , text="YOU WIN!" , font=( "Berlin Sans FB" , 36 ) , text_color="white" )
    finalWindow_communicationLabel.pack( pady=12 , padx=10 , expand=True )



    #* inizializzazione di un pulsante che permette all'utente di cominciare a giocare di nuovo
    finalWindow_playAgainButton = customtkinter.CTkButton( master=finalWindow_beautyFrame , text="PLAY AGAIN" , font=( "Berlin Sans FB" , 18 ) , command=main )
    finalWindow_playAgainButton.pack( pady=12 , padx=10 , expand=True )



    finalWindow.mainloop()



# separatore



def drawPlayerTable_withHits():
    #? funzione che disegna la tabella dell'utente e i colpi subiti 

    global playerTableFrame_container

    #* inizializzazione di un frame (per ragione grafiche)
    global playerTableFrame
    playerTableFrame = customtkinter.CTkFrame( master=playerTableFrame_container )
    playerTableFrame.pack( pady=12 , padx=10 )



    #* disegnamento della tabella (e dei riferimenti delle colonne e delle righe)
    global userShipPlacementSelection_Window_playerTable
    riferimentiColonne = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] # lo " " è utilizzato per dare la possibilità di posizionare anche i riferimenti per le righe
    riferimentiRighe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    for row in range(11):

        for column in range(11):

            if row == 0: # scrittura del riferimento delle colonne
                cell = customtkinter.CTkLabel( master=playerTableFrame , width=25 , text=riferimentiColonne[column] , font=( "Berlin Sans FB" , 18 ) )
            
            elif column == 0: # scrittura del riferimento delle righe
                cell = customtkinter.CTkLabel( master=playerTableFrame , width=25 , text=str( riferimentiRighe[row-1] ) , font=( "Berlin Sans FB" , 18 ) )

            else: # scrittura del contenuto di una determinata casella
                cell = customtkinter.CTkLabel( master=playerTableFrame , width=25 , text=userShipPlacementSelection_Window_playerTable[row-1][column-1] , font=( "Berlin Sans FB" , 18 ) )
        
            cell.grid( row=row , column=column )



# separatore



def drawNpcTable_withHits():
    #? funzione che disegna la tabella del npc e i colpi subiti

    global npcTableFrame_container

    #* inizializzazione di un frame per ragioni estetiche
    global npcTableFrame
    npcTableFrame = customtkinter.CTkFrame( master=npcTableFrame_container )
    npcTableFrame.pack( pady=12 , padx=10 )



    #* disegnamento della tabella (e dei riferimenti delle colonne e delle righe)
    global npcTable_onlyHits
    riferimentiColonne = [" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"] # lo " " è utilizzato per dare la possibilità di posizionare anche i riferimenti per le righe
    riferimentiRighe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for row in range(11):

        for column in range(11):

            if row == 0: #? scrittura del riferimento delle colonne
                cell = customtkinter.CTkLabel( master=npcTableFrame , width=25 , text=riferimentiColonne[column] , font=( "Berlin Sans FB" , 18 ) )
            
            elif column == 0: #? scrittura del riferimento delle righe
                cell = customtkinter.CTkLabel( master=npcTableFrame , width=25 , text=str( riferimentiRighe[row-1] ) , font=( "Berlin Sans FB" , 18 ) )

            else: #? scrittura del contenuto di una determinata casella (o cella)
                cell = customtkinter.CTkLabel( master=npcTableFrame , width=25 , text=npcTable_onlyHits[row-1][column-1] , font=( "Berlin Sans FB" , 18 ) )
        
            cell.grid( row=row , column=column )



# separatore



def playGame_Window_placeInputObjects():
    #? funzione che inizializza una cella di input e un pulsante

    global playGameWindow_beautyFrame

    # queste variabili sono rese globali per renderne possibile la distruzione
    global separator_1, coordinatesInput_beautyFrame, coordinatesEntry, hitButton, separator_2
    


    #* inizializzazione di un separatore
    separator_1 = customtkinter.CTkLabel( master=playGameWindow_beautyFrame , text="        " )
    separator_1.grid( row=1 , column=2 )



    #* inizializzazione di un frame (per ragioni grafiche)
    coordinatesInput_beautyFrame = customtkinter.CTkFrame( master=playGameWindow_beautyFrame )
    coordinatesInput_beautyFrame.grid( row=1 , column=3 )
    


    #* inizializzazione della cella di input 
    global chosen_coord
    chosen_coord = customtkinter.StringVar()

    coordinatesEntry = customtkinter.CTkEntry( master=coordinatesInput_beautyFrame , font=( "Berlin Sans FB" , 18 ) , textvariable=chosen_coord )
    coordinatesEntry.grid( row=0 , column=0 )



    #* inizializzazione del pulsante di attacco
    hitButton = customtkinter.CTkButton( master=coordinatesInput_beautyFrame , text="HIT!" , font=( "Berlin Sans FB " , 24 , "bold" ) , command=playGame_Window_hitAndUpdate )
    hitButton.grid( row=2 , column=0 )



    #* inizializzazione di un separatore
    separator_2 = customtkinter.CTkLabel( master=playGameWindow_beautyFrame , text="        " )
    separator_2.grid( row=1 , column=4 )



# separatore



def playGame_Window_hitAndUpdate():
    #? funzione che colpisce nelle coordinate scelte dall'utente, fa colpire l' npc e aggiorna la finestra

    #* traduzione delle coordinate inserite dall'utente e lancio del colpo + controllo della tabella per possibile vittoria dell'utente
    global npcTable, npcTable_onyHits, chosen_coord
    hit_x, hit_y = tools.translateCoords( chosen_coord.get() )

    audioPlayer.mixer.Sound( "./Sound Effects/Missile Blast.wav" ).play()

    if npcTable[hit_y][hit_x] != "X" and npcTable[hit_y][hit_x] != " ": # se l'utente colpisce una casella NON colpita in precedenza --> si procede con i test

        if npcTable[hit_y][hit_x] == "O": # se il colpo dell'utente va a segno --> l'utente continua a colpire

            npcTable[hit_y][hit_x] = "X"
            npcTable_onlyHits[hit_y][hit_x] = "X"
            audioPlayer.mixer.Sound( "./Sound Effects/Explosion.wav" ).play()

            userWin = tools.checkTable( npcTable )
            if userWin == True: # se l'utente a vinto
                winGame()

        else:
            # se l'utente manca il colpo, la tabella viene comunque aggiornata
            npcTable[hit_y][hit_x] = " "
            npcTable_onlyHits[hit_y][hit_x] = " "
            audioPlayer.mixer.Sound( "./Sound Effects/Splash.wav" ).play()

            hitCounter = 0
            while True:    

                #* generazione di una posizione nella quale l' npc andrà a colpire + controllo della tabella per possibile sconfitta dell'utente
                    #? questa eccezione if-else costituisce "l'intelligenza" del programma
                if hitCounter == 0:
                    hit_x, hit_y, = generate.randint( 0 , 9 ) , generate.randint( 0 , 9 )
                
                else:
                    #* se è il primo colpo dopo il colpo riuscito precedente, viene generata una direzione nel quale il programma continuerà a colpire
                    if hitCounter == 1:
                            rotation = generate.randint( 0 , 3 )
                        
                    if rotation == 0 and hit_y != 9: # su
                            hit_y += 1
                    elif rotation == 1 and hit_x != 9: # destra
                            hit_x += 1
                    elif rotation == 2 and hit_y != 0: # giù
                            hit_y -= 1
                    elif rotation == 3 and hit_x != 0: # sinistra
                            hit_x -= 1
                    
                    else: # se ci si trova all'estremità di una tabella
                        hit_x, hit_y, = generate.randint( 0 , 9 ), generate.randint( 0 , 9 )

                hitCounter += 1
                if userShipPlacementSelection_Window_playerTable[hit_y][hit_x] == "O": #* se il colpo è andato a segno
                    userShipPlacementSelection_Window_playerTable[hit_y][hit_x] = "X"
                    
                    userLose = tools.checkTable(userShipPlacementSelection_Window_playerTable)
                    if userLose == True:
                        loseGame()
                
                elif userShipPlacementSelection_Window_playerTable[hit_y][hit_x] == "~": #* se il colpo non è andato a segno
                    userShipPlacementSelection_Window_playerTable[hit_y][hit_x] = " "
                    break # viene concluso il ciclo di turni che l'npc avrebbe fatto se avesse continuato a colpire

                else: # le coordinate generate indicano una casella già colpita
                    hit_x, hit_y, = generate.randint( 0 , 9 ) , generate.randint( 0 , 9 )



        #* aggiornamento della finestra (distruzione elementi obsoleti e inizializzazione di elementi aggiornati)
        global playerTableFrame, npcTableFrame
        global coordinatesInput_beautyFrame
        
        playerTableFrame.destroy()
        npcTableFrame.destroy()

        coordinatesInput_beautyFrame.destroy()

        drawPlayerTable_withHits()
        drawNpcTable_withHits()
        playGame_Window_placeInputObjects()



# separatore



def playGame():
    #? funzione che consente all'utente di giocare

    global playGame_Window

    #* inizializzazione della finestra
    playGame_Window = customtkinter.CTk()
    playGame_Window.geometry( "850x500" )                       # definizione delle dimensioni
    playGame_Window.title( "Battleship" )                       # viene definito il titolo della finestra
    playGame_Window.resizable( width=False , height=False )     # viene impedito all'utente di cambiare le dimensioni della finestra
    playGame_Window.iconbitmap( "Battleship.ico" )              # viene utilizzato il file "Battleship.ico" come icona del software



    #* inizializzazione di un frame per ragioni estetiche
    global playGameWindow_beautyFrame
    playGameWindow_beautyFrame = customtkinter.CTkFrame( master=playGame_Window )
    playGameWindow_beautyFrame.pack( pady=12 , padx=10 , fill="both" , expand=True )

    

    #* inizializzazione di una sezione di "tutorial"
    playGameWindow_communicationLabel_symbolMeaning = customtkinter.CTkLabel( master=playGameWindow_beautyFrame , text="\nX = Successful hit;\n '  ' = Unsuccessful hit\n" , \
                                                                              font=( "Berlin Sans FB" , 18 ) )
    playGameWindow_communicationLabel_symbolMeaning.grid( row=0, column=3 )



    #! sezione giocatore
        #* inizializzazione di un frame per ragioni estetiche
    global playerTableFrame_container
    playerTableFrame_container = customtkinter.CTkFrame( master=playGameWindow_beautyFrame )
    playerTableFrame_container.grid( row=1 , column=1 )



        #* inizializzazione di un label che indica all'utente che tabella sta guardando
    global playerTableIndicator
    playerTableIndicator = customtkinter.CTkLabel( master=playerTableFrame_container , text="Your Table: " , font=( "Berlin Sans FB" , 18 ) )
    playerTableIndicator.pack( pady=12 , padx=10 )



    #! sezioine NPC
        #* inizializzazione di un frame (per ragioni grafiche)
    global npcTableFrame_container
    npcTableFrame_container = customtkinter.CTkFrame( master=playGameWindow_beautyFrame )
    npcTableFrame_container.grid( row=1 , column=5 )



        #* inizializzazione di un label che indica all'utente che tabella sta guardando
    global npcTableIndicator
    npcTableIndicator = customtkinter.CTkLabel( master=npcTableFrame_container , text="Enemy Table: " , font=( "Berlin Sans FB" , 18 ) )
    npcTableIndicator.pack( pady=12 , padx=10 )



    #* inizializzazione di un separatore che stacca la tabella contenente le navi dell'utente dal bordo della finestra
    borderSep = customtkinter.CTkLabel( master=playGameWindow_beautyFrame , text="       " )
    borderSep.grid( row=0 , column=0 )



    #* disegnamento della tabella dell'utente e del NPC (con gli eventuali colpi)
    drawPlayerTable_withHits()
    drawNpcTable_withHits()



    #* posizionamento della cella di input e del pulsante di conferma delle coordinate
    playGame_Window_placeInputObjects()



    playGame_Window.protocol( "WM_DELETE_WINDOW", exit )
    playGame_Window.mainloop()






# CODE-SECT: esecuzione del codice
def main():

    finalWindow.destroy()
    global difficulty, npcTable, npcTable_onlyHits, userShipPlacementSelection_Window_playerTable

    #! scelta della difficoltà
    difficulty = "Easy" # viene inizializzata la difficoltà di default del gioco
    difficultySelection()

    audioPlayer.init()
    if difficulty == "Easy" or difficulty == "Medium":
        audioPlayer.mixer.music.load( "./Music/Along With Waves.wav" )
        audioPlayer.mixer.music.set_volume( 0.3 )
    
    elif difficulty == "Hard":
        audioPlayer.mixer.music.load( "./Music/Delirious Bite.wav" )
        audioPlayer.mixer.music.set_volume( 0.3 )
    
    elif difficulty == "Hell":
        audioPlayer.mixer.music.load( "./Music/Troubled Mind.wav" )
        audioPlayer.mixer.music.set_volume( 0.3 )

    audioPlayer.mixer.music.play( loops=-1 )

    #! posizionamento delle navi
    npcTable = tools.randomPlaceShips( tools.initTabella() , difficulty ) # viene inizializzata e riempita la tabella del computer (npc = non player character = personaggio non giocante)
    npcTable_onlyHits = tools.initTabella() # viene inizializzata e riempita la tabella che conterrà i colpi tirati dall'utente ai danni del npc

    userShipPlacementSelection_Window_playerTable = tools.randomPlaceShips( tools.initTabella() , difficulty ) # viene inizializzata e riempita la tabella dell'utente
    shipPlacementSelection()
    playGame()

    audioPlayer.mixer.quit()

finalWindow = customtkinter.CTk() # questa finestra viene inizializzata ma non mandata in loop per permettere al main di distruggerla anche all'avvio della prima partita
main()