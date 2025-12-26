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
    try:
        while True:
            show_menu()
            print("\n")
            choice = input("Keuze: ")
            
            if choice == '1':
                optie1(db)
                
            elif choice == '2':   
                optie2(db)
    
            elif choice == '3':
                optie3(db)
                
            elif choice == '4':
                optie4(db)

            elif choice == '5':
                zoekterm = input("Zoek op merk of model: ")
                cursor = db.execute(
                    """
                    SELECT id, merk, model, productiedatum, prijs, vinnummer
                    FROM brommers
                    WHERE merk LIKE ? OR model LIKE ?
                    """,
                    (f"%{zoekterm}%", f"%{zoekterm}%")
                )
                resultaten = cursor.fetchall()
                if resultaten:
                    print("\nGevonden brommers:")
                    for b in resultaten:
                        print(
                            f"ID: {b[0]} | Merk: {b[1]} | Model: {b[2]} | "
                            f"Productiedatum: {b[3]} | Prijs: €{b[4]} | VIN: {b[5]}"
                        )
                else:
                    print("Geen brommers gevonden met deze zoekterm.")

            elif choice == '6':
                cursor = db.execute(
                    "SELECT id, merk, model, productiedatum, prijs, vinnummer FROM brommers"
                )
                brommers = cursor.fetchall()
                if not brommers:
                    print("Geen brommers om te exporteren.")
                else:
                    with open("overzicht_brommers.txt", "w", encoding="utf-8") as file:
                        file.write("OVERZICHT BROMMERS\n")
                        file.write("=" * 50 + "\n\n")
                        for b in brommers:
                            file.write(
                                f"ID: {b[0]}\n"
                                f"Merk: {b[1]}\n"
                                f"Model: {b[2]}\n"
                                f"Productiedatum: {b[3]}\n"
                                f"Prijs: €{b[4]}\n"
                                f"VIN: {b[5]}\n"
                                + "-" * 50 + "\n"
                            )
                print("Overzicht succesvol opgeslagen in 'overzicht_brommers.txt'")

            elif choice == '0':
                print("\nProgramma wordt afgesloten.")
                break
                db.close()
                
            else:
                print("Voer een nummer in van 0-6")
            
    except KeyboardInterrupt:
        print("\n\nProgramma wordt afgesloten.")
        db.close()
    
    
def optie1(db):
    print("------------------------------------------")
    print("OVERZICHT")
    cursor = db.execute(
        "SELECT id, merk, model, productiedatum, prijs, vinnummer FROM brommers"
    )
    for b in cursor.fetchall():
        print(f"ID: {b[0]} | Merk: {b[1]} | Model: {b[2]} | "
              f"Productiedatum: {b[3]} | Prijs: €{b[4]} | VIN: {b[5]}")


def optie2(db):
    print("------------------------------------------")
    print("BROMMER TOEVOEGEN")
    while True:
        merk = input("Merk: ").strip()
        if merk:
            break
        print("Merk mag niet leeg zijn.")
    while True:
        model = input("Model: ").strip()
        if model:
            break
        print("Model mag niet leeg zijn.")
    while True:
        productiedatum = input("Productiedatum (YYYY-MM-DD): ").strip()
        if productiedatum:
            break
        print("Productiedatum mag niet leeg zijn.")
    while True:
        prijs_input = input("Prijs: ").strip()
        try:
            prijs = float(prijs_input)
            break
        except ValueError:
            print("Ongeldige prijs. Voer een geldig getal in.")
    while True:
        vinnummer = input("Vinnummer: ").strip()
        if vinnummer:
            break
        print("Vinnummer mag niet leeg zijn.")
    db.execute(
        "INSERT INTO brommers (merk, model, productiedatum, prijs, vinnummer) "
        "VALUES (?, ?, ?, ?, ?)",
        (merk, model, productiedatum, prijs, vinnummer)
    )
    print("Brommer toegevoegd.")


def optie3(db):
    print("------------------------------------------")
    print("BROMMER WIJZIGEN")
    brommer_id = input("ID van de brommer die je wilt wijzigen: ")
    cursor = db.execute("SELECT * FROM brommers WHERE id=?", (brommer_id,))
    brommer = cursor.fetchone()

    if brommer:
        print(f"Wijzig brommer: {brommer[1]} {brommer[2]} (ID: {brommer[0]})")
        merk = input(f"Nieuw merk [{brommer[1]}]: ") or brommer[1]
        model = input(f"Nieuw model [{brommer[2]}]: ") or brommer[2]
        productiedatum = input(f"Nieuwe productiedatum [{brommer[3]}]: ") or brommer[3]
        while True:
            prijs_input = input(f"Nieuwe prijs [{brommer[4]}]: ")
            if not prijs_input:  # Enter ingedrukt, geen wijziging
                prijs = brommer[4]
                break
            try:
                prijs = float(prijs_input)
                break
            except ValueError:
                print("Ongeldige prijs. Voer een geldig getal in")
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


def optie4(db):
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
                      
if __name__ == '__main__':
    main()