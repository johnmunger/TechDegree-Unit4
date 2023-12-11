from Constants import *
from PrintHelpers import space
from inventory import Brand, Product, session


def _view_product():
    view_flag = True
    while view_flag:
        print(
            """\n
            \nPRODUCT MANAGEMENT\n
            \rV)iew Product\n
            \rN)ew Product\n
            \rD)elete Product\n
            \rR)eturn to Main Menu\n
            """
        )
        viewChoice = input("Select an Option: ").upper()
        if viewChoice in PRODUCT_MANAGEMENT_OPTIONS:
            if viewChoice == "V":
                working = True
                while working:
                    try:
                        selectedProduct = _get_product()
                        if selectedProduct:
                            brand = (
                                session.query(Brand)
                                .filter(Brand.brand_id == selectedProduct.brand_id)
                                .one()
                            )
                            space()
                            for i in range(len(PRODUCT_COLUMN_NAMES)):
                                print(
                                    f"{PRODUCT_COLUMNS_ALIASED[i]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[i])}"
                                )
                            print(f"Brand name: {brand.brand_name}")
                            editSelection = input("Would you like to E)dit, D)elete record,or P)ass?").upper()
                            if(editSelection in EDIT_OPTIONS):
                                if editSelection == "E":
                                    editing = True
                                    while editing:
                                        try:
                                            print('Select one of the following columns, or R to return to Product Management menu')
                                            space()
                                            for i,v in enumerate(PRODUCT_COLUMNS_ALIASED):
                                                print(f'{i}) {v}')
                                            k = input(" : ")
                                            if k.upper() == 'R':
                                                break
                                            k = int(k)
                                            value = input(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")

                                            selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],value)
                                            try:
                                                session.commit()
                                                print(f'{getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])} updated successfully')
                                            except:
                                                session.rollback()
                                                "Commit Failure.  Rolling Back Changes"
                                            
                                        except:
                                            print(f"Please enter an integer between 1 and {len(PRODUCT_COLUMN_NAMES)}")
                                if editSelection == "D":
                                    deleting = True
                                    while deleting:
                                        try:
                                            answer = input("Are you sure you want to delete product?").upper()
                                            if answer in DELETE_OPTIONS:
                                                if answer == 'Y':
                                                    session.delete(selectedProduct)
                                                else:
                                                    deleting = False
                                            else:
                                                raise Exception
                                        except:
                                            print("Please Enter Y or N")
                                if editSelection == "P":
                                    break
                            else:
                                print("Please Enter either E, D, or P")

                            break
                        raise Exception()
                    except:
                        print("Please Enter INTEGER value of product_id")
            if viewChoice == "N":
                try:
                    selectedProduct = _get_product()
                except:
                    print("Please Enter INTEGER value of product_id")

            if viewChoice == "R":
                break
        else:
            print("Please Enter the letters V, N, D, or R")

def _get_product():
    read_input = input("Enter Product Id.")
    return session.query(Product).filter(Product.product_id == read_input).one_or_none()

def editOrDelete(selectedProduct):
    pass


_view_product()