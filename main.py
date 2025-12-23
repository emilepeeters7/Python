def show_menu():
    print("\n")
    print("##########################################")
    print("#  1) Overzicht                          #")
    print("#  2) Brommer toevoegen                  #")
    print("#  3) Brommer wijzigen                   #")
    print("#  3) Brommer wijzigen                   #")
    print("#  4) Brommer verwijderen/verkocht       #")
    print("#  5) Brommer zoeken op merk of model    #")
    print("#  6) Overzicht printen naar een file    #")
    print("#  0) Exit                               #")
    print("##########################################")
    
def main():
    while True:
        show_menu()
        print("\n")
        choice = input("Keuze: ")

        if choice == '1':
            break
        elif choice == '2':   
            break
        elif choice == '3':
            break
        elif choice == '4':
            break
        elif choice == '5':
            break
        elif choice == '0':
            break
            
        else:
            print("Je hebt enkel de keuze tussen bovenstaande opties (0-5)")
                
            
if __name__ == '__main__':
    main()