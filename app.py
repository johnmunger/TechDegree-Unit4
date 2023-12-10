from inventory import BASE, ENGINE, Product, importBrands, importProducts, session


def app():
    appRunning = True
    while appRunning:
        print(
            """
              \nPROGRAMMING BOOKS
              \rV)iew Product
              \rN)ew Product
              \rA)nalyze Product
              \rB)ackup Database
              \rQ)uit
              """
        )
        mainMenuChoice = input("What would you like to do?\n\n").upper()
        if mainMenuChoice in {"V", "N", "A", "B", "Q"}:
            if mainMenuChoice == "V":
                viewInput = input("Searching by product ID.  Enter Product Id. \n\n")
                selectedProduct = (
                    session.query(Product).filter(Product.product_id >= viewInput).first()
                )
                print("\n\n")
                print(selectedProduct)
                print("\n\n")
            if mainMenuChoice == "Q":
                appRunning = False
            else:
                print("Please Enter the letters V, N, A, or B.  To Quit Enter Q")
if __name__ == "__main__":
    BASE.metadata.create_all(ENGINE)
    importBrands(session)
    importProducts(session)
    app()