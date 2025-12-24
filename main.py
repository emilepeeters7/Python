from database import Database

def show_menu():
    print("\n")
    print("##########################################")
    print("#  1) Overzicht                          #")
    print("#  2) Brommer toevoegen                  #")
    print("#  3) Brommer wijzigen                   #")
    print("#  4) Brommer verwijderen/verkocht       #")
    print("#  5) Brommer zoeken op merk of model    #")
    print("#  6) Overzicht printen naar een file    #")
    print("#  0) Exit                               #")
    print("##########################################")  
def main():
    db = Database()
    while True:
        show_menu()
        print("\n")
        choice = input("Keuze: ")

        if choice == '1':
            print("------------------------------------------")
            print("OVERZICHT")
            cursor = db.execute(
                "SELECT id, merk, model, productiedatum, prijs, vinnummer FROM brommers"
            )
            for b in cursor.fetchall():
                print(f"ID: {b[0]} | Merk: {b[1]} | Model: {b[2]} | "
                      f"Productiedatum: {b[3]} | Prijs: €{b[4]} | VIN: {b[5]}")

            
            
            
        elif choice == '2':   
            print("------------------------------------------")
            print("BROMMER TOEVOEGEN")
            merk = input("Merk: ")
            model = input("Model: ")
            productiedatum = input("Productiedatum (YYYY-MM-DD): ")
            prijs = float(input("Prijs: "))
            vinnummer = input("Vinnummer: ")

            db.execute(
                "INSERT INTO brommers (merk, model, productiedatum, prijs, vinnummer) VALUES (?, ?, ?, ?, ?)",
                (merk, model, productiedatum, prijs, vinnummer)
            )
            print("Brommer toegevoegd.")

    


        elif choice == '3':
            brommer_id = input("ID van de brommer die je wilt wijzigen: ")
            cursor = db.execute("SELECT * FROM brommers WHERE id=?", (brommer_id,))
            brommer = cursor.fetchone()

            if brommer:
                print(f"Wijzig brommer: {brommer[1]} {brommer[2]} (ID: {brommer[0]})")

    
                merk = input(f"Nieuw merk [{brommer[1]}]: ") or brommer[1]
                model = input(f"Nieuw model [{brommer[2]}]: ") or brommer[2]
                productiedatum = input(f"Nieuwe productiedatum [{brommer[3]}]: ") or brommer[3]
                prijs_input = input(f"Nieuwe prijs [{brommer[4]}]: ")
                prijs = float(prijs_input) if prijs_input else brommer[4]
                vinnummer = input(f"Nieuwe VIN [{brommer[5]}]: ") or brommer[5]

                db.execute(
                    """
                    UPDATE brommers
                    SET merk=?, model=?, productiedatum=?, prijs=?, vinnummer=?
                    WHERE id=?
                    """,
                    (merk, model, productiedatum, prijs, vinnummer, brommer_id)
                )

                print("Brommer succesvol gewijzigd.")
            else:
                    print("Brommer met dit ID niet gevonden.")

            
            
                        
        elif choice == '4':
            brommer_id = input("ID van de brommer die je wilt verwijderen: ")
            cursor = db.execute("SELECT id, merk, model FROM brommers WHERE id=?", (brommer_id,))
            brommer = cursor.fetchone()

            if brommer:
                bevestiging = input(f"Weet je zeker dat je {brommer[1]} {brommer[2]} wilt verwijderen? (j/n): ")
                if bevestiging.lower() == 'j':
                    db.execute("DELETE FROM brommers WHERE id=?", (brommer_id,))
                    print("Brommer verwijderd.")
                else:
                    print("Verwijderen geannuleerd.")
            else:
                print("Brommer niet gevonden.")




        elif choice == '5':
            break
        elif choice == '0':
            break
            
        else:
            print("Je hebt enkel de keuze tussen bovenstaande opties (0-5)")
                
            
if __name__ == '__main__':
    main()