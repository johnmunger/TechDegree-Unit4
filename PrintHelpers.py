from Constants import PRODUCT_COLUMN_NAMES, PRODUCT_COLUMNS_ALIASED
from inventory import Product
def _space():
    print('\n')

def printPadding(string):
    print(string)
    _space()

def printProductWithBrandName(selectedProduct):
    brandName = selectedProduct.__getattribute__('brands.brand_id').__getattribute__('brand_name')
    _space()
    for i in range(len(PRODUCT_COLUMN_NAMES)):
        print(f"{PRODUCT_COLUMNS_ALIASED[i]}: {brandName}") if i == 5 else print(f"{PRODUCT_COLUMNS_ALIASED[i]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[i])}")
    _space()

def getInputInt(string):
    gettingInput = True
    while gettingInput:
        try:
            integer = int(input(string))
            _space()
            gettingInput = False
        except ValueError:
            printPadding("Please Enter Integer")
    return integer
def getInput(string):
    gettingInput = True
    while gettingInput:
        try:
            inputString = input(string)
            _space()
            gettingInput = False
        except:
            printPadding("Input failed try again")
    return inputString
