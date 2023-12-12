from Constants import MAIN_MENU_OPTIONS
from PrintHelpers import doubleSpace, space
from ProductController import view_product, new_product, analyse_products, backup_database
from inventory import BASE, ENGINE, import_brands, import_products, session


def app():
    app_running = True
    while app_running:
        print(
            """
              \nINVENTORY MENU\na
              \rV)iew Producta
              \rN)ew Product
              \rA)nalyze Product
              \rB)ackup Database
              \rQ)uit
              """
        )
        space()
        mainMenuChoice = input("What would you like to do?").upper()
        doubleSpace()
        if mainMenuChoice in MAIN_MENU_OPTIONS:
            if mainMenuChoice == "V":
                view_product()
            if mainMenuChoice == "N":
                new_product()
            if mainMenuChoice == "A":
                analyse_products()
            if mainMenuChoice == "B":
                backup_database()
            if mainMenuChoice == "Q":
                app_running = False
            else:
                print("Please Enter the letters V, N, A, or B.  To Quit Enter Q")

if __name__ == "__main__":
    BASE.metadata.create_all(ENGINE)
    import_brands(session)
    import_products(session)
    app()