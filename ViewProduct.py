from Constants import productColumnNames, productColumnsAliased
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
        if viewChoice in {"V", "N", "D", "R"}:
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
                            for i in range(len(productColumnNames)):
                                print(
                                    f"{productColumnsAliased[i]}: {getattr(selectedProduct, productColumnNames[i])}"
                                )
                            print(f"Brand name: {brand.brand_name}")
                            break
                        raise Exception()
                    except:
                        print("Please Enter INTEGER value of product_id")
            if viewChoice == "R":
                break
        else:
            print("Please Enter the letters V, N, D, or R")

def _get_product():
    read_input = input("Enter Product Id.")
    return session.query(Product).filter(Product.product_id == read_input).one_or_none()


_view_product()