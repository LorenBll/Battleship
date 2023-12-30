# Stumenti per Battleship.py

# CODE-SECT: funzioni utilizzate durante la fase di testing
def printTabella(tab):
    #? funzione di stampa della tabella di gioco
    
    print("  A B C D E F G H I J") # stampa degli indici di riferimento delle colonne

    for i in range(10):
        
        # stampa del riferimento delle righe con distanziamento dal contenuto stampato distinto in base allo spazio occupato
        if len( str( i+1 ) ) == 1:
            print( i , end=" " )
        else:
            print( i , end=" " )

        # stampa della riga
        for j in range(10):
            print( tab[i][j] , end=" " )
        print() # stampa di distacco







# CODE-SECT: funzioni utilizzate normalmente dal programma
def fileExists(file_name):
    #? funzione che verifica l'esistenza di un file

    try:
        #* si prova ad aprire il file in modalità di appendimento
        with open( file_name , "a" ) as file:
            pass
        return True # il file esiste
    
    except:
        return False # il codice del try dà errore --> il file non esiste



# separatore



def reportError(error_code):
    #? funzione che registra gli errori su un un file

    import customtkinter

    #! definizione dei codici di errori disponibili e dell'errore indicato
    errorCodesList = ["000", \
                    "001.0", \
                    "001.1", \
                    "002"]

    errorsList = ["too many letters used in the coordinates' input", \
                "the letter used in the coordinates' input indicates nothing", \
                "the number used in the coordinates' input indicates nothing", \
                "The given difficulty doesn't exist"]



    #! ottenimento e riscrittura della data e del momento corrente
    import datetime
    raw_date = str( datetime.datetime.now() )
    raw_date = raw_date.split( " " )
    day = raw_date[0].replace( "-" , "/" )
    moment = raw_date[1]



    #! scrittura dell'errore
    if fileExists( "ErrorLog.txt" ) == True:
        with open( "ErrorLog.txt" , "a" ) as register:
            register.write( "[" + day + " - " + moment + "]" + " : ERR-" + error_code + "   " + errorsList[errorCodesList.index(error_code)] + "\n" )

    else:
        with open( "ErrorLog.txt", "w" ) as register:
            register.write( "[" + day + " - " + moment + "]" + " : ERR-" + error_code + "   " + errorsList[errorCodesList.index(error_code)] + "\n" )



    #! inizializzazione di una finestra che segnala l'errore all'utente
    errorWindow = customtkinter.CTk()
    errorWindow.geometry( "500x100" )
    errorWindow.resizable( width=False, height=False ) # viene impedito all'utente di cambiare le dimensioni della finestra
    errorWindow.title( "Battleship: ERR-" + error_code )

    label = customtkinter.CTkLabel( master=errorWindow , text=( "An error occured during the execution of the program:\n" + "ERR-" + error_code + ": Search in 'ErrorLog.txt' for more informations" ) , font=( "Berlin Sans FB" , 18 ) )
    label.pack( pady=12 , padx=10 )

    errorWindow.mainloop()



# separatore



def initTabella():
    #? funzione di inizializzazione della tabella (10 * 10)
    
    tabella = []
    for i in range(10):
        
        riga = []
        for j in range(10):
            riga.append( "~" )

        tabella.append(riga)

    return tabella



# separatore



def translateCoords(human_coords):
    #? funzione di conversione di coordinate comprensibili all'uomo a coordinate comprensibili al programma

    human_coords = human_coords.upper() # conversione delle lettere inserite in lettere maiuscole
    listaLettere = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    n_lettere = 0 # contatore che indicherà il numero di lettere presenti nel parametro passato
    machine_y = "" # variabile di ritorno
    for i in range(len(human_coords)):

        #? riconoscimento della natura del carattere analizzato (lettera o numero)
        try:
            temp = int(human_coords[i])
            machine_y += str(temp)
        
        except:
            
            #* controllo sul parametro --> se ci sono troppe lettere, viene mandato in crash il programma
            if n_lettere == 1:
                reportError( "000" )
                return False
            
            else:
                n_lettere += 1

                #* controllo sulla lettera --> se non corrisponde a niente, viene mandato in errore il programma
                if human_coords[i] not in listaLettere:
                    reportError( "001.0" )
                    return False
                
                else:
                    machine_x = listaLettere.index(human_coords[i])

    #* passaggio da stringa ad intero delle coord-y (con diminuzione di 1 per rendere la coordinata elaborabile dalla macchina) + controllo sul valore --> se è maggiore di 9 (10 per l'uomo) o minore di 0, viene mandato in crash il programma
    machine_y = int(machine_y) - 1
    if machine_y > 9 or machine_y < 0:
        reportError( "001.1" )
        return False

    return machine_x, machine_y # il riferimento dell'utente è diverso dal riferimento della macchina



# separatore



def columnLister(tab, x_coord):
    #? funzione che genera una lista corrispondente alla colonna n° x_coord passata

    colonna = []
    for i in range(len(tab)):
        colonna.append(tab[i][x_coord])

    return colonna



# separatore



def randomPlaceShips(tab, diff):
    #? funzione che piazza in posizione casuali delle navi

    #! conversione della difficoltà passata in un numero
    listDiff = ["Easy", "Medium", "Hard", "Hell"]
    diff = listDiff.index(diff)



    #! inizializzazione delle liste contenenti le dimensioni delle navi e del numero di navi di una data dimensione da posizionare
    dimNavi = [5, 4, 3, 2, 1] # lista contenente le dimensioni della navi
    
    listNumNavi = [[3, 4, 0, 0, 0], [2, 2, 3, 0, 0], [1, 1, 2, 3, 0], [0, 0, 1, 2, 4]]
    numNavi = listNumNavi[diff] # lista contenente le dimensioni delle navi da piazzare



    #! calcolo della posizione e posizionamento delle navi
    import random as gen

    for i in range(5): # 5 = tipi possibili di nave

        for j in range( numNavi[i] ):

            #? calcolo del punto di generazione iniziale e controllo sulle celle da riempire
            while True:
                
                #* generazione della posizione di generazione iniziale e della rotazione della nave + ri-definizione della dimensione per maggior leggibilità
                y_coord = gen.randint( 0 , 9 )
                x_coord = gen.randint( 0 , 9 )

                rotation = gen.randint( 0 , 1 ) # 0 = su, 1 = sinistra
                dimensione = dimNavi[i]



                #* controllo sulle celle da occupare + posizionamento della nave
                libero = False

                if rotation == 0: #? la nave è ruotata verso l'alto 
                    
                    #! controlli sulle celle da occupare
                    # controllo sullo spazio disponibile (sia occupato che non)
                    colonna = columnLister(tab, x_coord)
                    spazio_disponibile = y_coord

                    if spazio_disponibile >= dimensione: # la nave è sufficientemente piccola da starci --> si prosegue con i test

                        # verifica della disoccupazione delle celle che verrano riempite
                        sezioneTab = colonna[:y_coord]
                        sezioneTab.reverse()
                        for k in range(dimensione):
                            if sezioneTab[k] == "~":
                                libero = True #* la nave si può posizionare

                            else:
                                libero = False #* la nave non si può posizionare
                                break
                                
                    else: # la nave è troppo grande --> non viene eseguito nessun'altro test
                        pass
                
                    #! posizionamento della nave
                    if libero == True:
                        for k in range(dimensione):

                            tab[y_coord][x_coord] = "O"
                            y_coord -= 1

                        break #* la nave è stata generata completamente



                if rotation == 1: #? la nave è ruotata verso sinistra

                    #! controlli sulle celle da occupare
                    # controllo sullo spazio disponibile (sia occupato che non)
                    riga = tab[y_coord].copy()
                    spazio_disponibile = x_coord

                    if spazio_disponibile >= dimensione: # la nave è sufficientemente piccola da starci --> si prosegue con i test

                        # verifica della disoccupazione delle celle che verranno riempite
                        sezioneTab = riga[:x_coord]
                        sezioneTab.reverse()
                        for k in range(dimensione):
                            if sezioneTab[k] == "~":
                                libero = True #* la nave si può posizionare

                            else:
                                libero = False #* la nave non si può posizionare
                                break

                    else: # la nave è troppo grande --> non viene eseguito nessun'altro test
                        pass

                    #! posizionamento della nave
                    if libero == True:
                        for k in range(dimensione):

                            tab[y_coord][x_coord] = "O"
                            x_coord -= 1

                        break #* la nave è stata generata completamente

    return tab



# separatore



def checkTable(tab):
    #? funzione che controlla se su una tabella non è presente nessuna casella occupata e NON colpita

    for row in range(10):
        for column in range(10):

            if tab[row][column] == "O":
                return False # il gioco può continuare

    return True # il gioco si deve fermare --> qualcuno ha vinto