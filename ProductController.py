import datetime
import csv
from Constants import *
from PrintHelpers import doubleSpace, space
from inventory import Brand, Product, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def view_product():
    working = True
    while working:
        try:
            selectedProduct = _get_product()
            if selectedProduct:
                brandName = selectedProduct.__getattribute__('brands.brand_id').__getattribute__('brand_name')
                for i in range(len(PRODUCT_COLUMN_NAMES)):
                    print(f"{PRODUCT_COLUMNS_ALIASED[i]}: {brandName}") if i == 5 else print(f"{PRODUCT_COLUMNS_ALIASED[i]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[i])}")
                editSelection = input("Would you like to E)dit, D)elete record,or P)ass?").upper()
                if(editSelection in EDIT_OPTIONS):
                    if editSelection == "E":
                        editing = True
                        while editing:
                            """ try: """
                            print('Select one of the following columns, or R to return to Product Management menu')
                            space()
                            for i,v in enumerate(PRODUCT_COLUMNS_ALIASED):
                                if(i != 0):
                                    print(f'{i}) {v}')
                            k = input(" : ")
                            if k.upper() == 'R':
                                break
                            k = int(k)

                            if(PRODUCT_COLUMNS_ALIASED[k] == "Product Price"):
                                value = input(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")
                                try:
                                    value = format_price(value)
                                except TypeError as e:
                                    print(e)
                                except ValueError as e:
                                    print(e)

                            elif (PRODUCT_COLUMNS_ALIASED[k] == "Date Updated"):
                                value = input("Enter Date in YYYY:MM:DD format")
                                try:
                                    value = format_date(value, selectedProduct)
                                except ValueError as e:
                                    print(e)

                            elif(PRODUCT_COLUMNS_ALIASED[k] == 'Brand Name'):
                                value = input(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")
                                try:
                                    newBrand = (
                                    session.query(Brand)
                                    .filter(Brand.brand_name == value)
                                    .one()
                                    )
                                    selectedProduct.brand_id = newBrand.brand_id
                                except NoResultFound as e:
                                    print(e)
                                except MultipleResultsFound as e:
                                    print(e)
                                else:
                                    selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],newBrand.brand_id)
                                    print(f'{PRODUCT_COLUMNS_ALIASED[k]} updated successfully')
                                    break
                            else:
                                value = input(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")

                            selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],value)

                            try:
                                session.commit()
                                print(f'{PRODUCT_COLUMNS_ALIASED[k]} updated successfully')
                            except:
                                session.rollback()
                                "Commit Failure.  Rolling Back Changes"

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
        except TypeError as e:
            print(e)

def format_price(price):
    try:
        price = float(price)
        return price
    except TypeError:
        print("TypeError")
    except ValueError:
        print("ValueError")
def format_date(date, selectedProduct):
    dateArray = date.split('-')
    dateDate = datetime.date(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]))
    if(selectedProduct.date_updated):
        if(dateDate >= selectedProduct.date_updated):
            return dateDate
        elif(dateDate < selectedProduct.date_updated):
            raise ValueError("Please...can you just...do it right this time???? Look at date updated...c'mon.")
    else:
        return dateDate

def new_product():
    addingNew = True
    while addingNew:
        newProduct = Product()
        for i, v in enumerate(PRODUCT_COLUMNS_ALIASED):
            if(i != 0):
                if PRODUCT_COLUMNS_ALIASED[i] == 'Product Price':
                    value = input(f"{v}:")
                    try:
                        value = format_price(value)
                    except TypeError as e:
                        print(e)
                    except ValueError as e:
                        print(e)
                    else:
                        newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)
                elif PRODUCT_COLUMNS_ALIASED[i] == 'Date Updated':
                    value = input("Enter Date in YYYY-MM-DD format: ")
                    try:
                        value = format_date(value, newProduct)
                        newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)
                    except ValueError as e:
                        print(e)      
                elif PRODUCT_COLUMNS_ALIASED[i] == 'Brand Name':
                    value = input(f"{PRODUCT_COLUMNS_ALIASED[i]}")
                    try:
                        newBrand = (session.query(Brand)
                        .filter(Brand.brand_name == value)
                        .one()
                        )
                        newProduct.brand_id = newBrand.brand_id
                    except NoResultFound as e:
                        print(e)
                    except MultipleResultsFound as e:
                        print(e)
                else:
                    value = input(f"{PRODUCT_COLUMN_NAMES[i]}:")
                    newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)

        try:
            session.add(newProduct)
            session.commit()
            space()
            print(f'{newProduct} updated successfully')
            addingNew = False
            
        except IntegrityError as e:
            space()
            print(e)
            session.rollback()
            print("Commit Failure.  Rolling Back Changes")

def _get_product():
    read_input = input("Enter Product Id.")
    return session.query(Product).join(Brand).filter(Product.product_id == read_input).one()

def analyse_products():
    analyzing = True
    while analyzing:
        doubleSpace()
        print('ANALYSIS MODE ENGAGED: ')
        space()
        for i, v in enumerate(ANALYSIS_OPTIONS):
           print(f'{i+1}: {v}')
        itsANumber = int(input("pick "))
        
        if itsANumber == 1:
            print(f'{session.query(Product).order_by(Product.product_price.desc()).first()}')
        elif itsANumber == 2:
            print(f'{session.query(Product).order_by(Product.product_price).first()}')
        elif itsANumber == 3:
           """  productBrands = session.query(Product).join(Brand).all()
            brandDictionary = {}
            for v in productBrands:
                brandName = v.__getattribute__('brands.brand_id').__getattribute__('brand_name')
                if(brandDictionary[brandName]):
                   
            
            topKey=''
            topValue=0
            for k, v in brandDictionary.items():   
                if v > topValue:
                    topKey=k
                    topValue=v """
           pass

                    
                
                

                
                

        elif itsANumber == 4:
            print(f'{session.query(Product).order_by(Product.date_updated.desc()).first()}')
        elif itsANumber == 5:
            print(f'{session.query(Product).order_by(Product.date_updated).first()}')
        elif itsANumber == 6:
            print(f'{session.query(Product).order_by(Product.product_quantity.desc()).first()}')
        answer = input('Done. Y)es or N)o? ').upper()

        if answer == 'Y':
            break
        if answer == 'N':
            pass
    
    
    
def backup_database():
    productBrands = session.query(Product).join(Brand).all()

    with open('inventory2.csv', 'w', newline='') as csvfile:
        rowWriter = csv.writer(csvfile, delimiter=',')
        rowWriter.writerow(PRODUCT_BRAND_CSV_COLUMN_NAMES)
        for v in productBrands:
            brandName = v.__getattribute__('brands.brand_id').__getattribute__('brand_name')
            rowWriter.writerow([v.product_id,v.product_name,v.product_price,v.product_quantity,v.date_updated, brandName])
