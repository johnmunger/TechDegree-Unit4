from PrintHelpers import doubleSpace, space
from ViewProduct import viewProduct
from inventory import BASE, ENGINE, Product, importBrands, importProducts, session


def app():
    app_running = True
    while app_running:
        print(
            """
              \nINVENTORY MENU\n
              \rV)iew Product
              \rN)ew Product
              \rA)nalyze Product
              \rB)ackup Database
              \rQ)uit
              """
        )
        space()
        mainMenuChoice = input("What would you like to do?").upper()
        doubleSpace()
        if mainMenuChoice in {"V", "N", "A", "B", "Q"}:
            if mainMenuChoice == "V":
                viewProduct()
            if mainMenuChoice == "N":
                _new_product()
            if mainMenuChoice == "Q":
                pass
            else:
                print("Please Enter the letters V, N, A, or B.  To Quit Enter Q")


def _new_product():
    product = Product()
    for i in range(len(product_columns)):
        attr = input(f"Enter {product_columns[i]}")
        product.__setattr__(product_columns[i], attr)
if __name__ == "__main__":
    BASE.metadata.create_all(ENGINE)
    importBrands(session)
    importProducts(session)
    app()