from datetime import date, datetime
import csv
from Constants import *
from PrintHelpers import getInput, getInputInt, printPadding, printProductWithBrandName
from inventory import Brand, Product, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def view_product():
    viewing = True
    while viewing:
        selectedProduct = _get_product()
        if selectedProduct:
            printProductWithBrandName(selectedProduct)
            editSelection = getInput("Would you like to E)dit, D)elete record,or P)ass?").upper()
            if(editSelection in EDIT_OPTIONS):
                if editSelection == "E":
                    editing = True
                    while editing:
                        for i,v in enumerate(PRODUCT_COLUMNS_ALIASED):
                            if(i != 0):
                                print(f'{i}) {v}')
                        k = getInputInt("?: ")
                        if(PRODUCT_COLUMNS_ALIASED[k] == "Product Price"):
                            value = getInput(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")
                            value = format_price(value)
                            selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],value)

                        elif (PRODUCT_COLUMNS_ALIASED[k] == "Date Updated"):
                            value = getInput("Enter Date in YYYY:MM:DD format")
                            try:
                                value = format_date(value, selectedProduct)
                            except ValueError as e:
                                getInput(e)
                            selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],value)

                        elif(PRODUCT_COLUMNS_ALIASED[k] == 'Brand Name'):
                            brandName = selectedProduct.__getattribute__('brands.brand_id').__getattribute__('brand_name')
                            value = getInput(f"{PRODUCT_COLUMNS_ALIASED[k]}: {brandName}\nUpdated Value: ")
                            try:
                                newBrand = (
                                session.query(Brand)
                                .filter(Brand.brand_name == value)
                                .one()
                                )
                                selectedProduct.brand_id = newBrand.brand_id
                            except NoResultFound as e:
                                getInput(e)
                            except MultipleResultsFound as e:
                                getInput(e)
                            else:
                                selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],newBrand.brand_id)
                                printPadding(f'{PRODUCT_COLUMNS_ALIASED[k]} updated successfully')
                        else:
                            value = getInput(f"{PRODUCT_COLUMNS_ALIASED[k]}: {getattr(selectedProduct, PRODUCT_COLUMN_NAMES[k])}\nUpdated Value: ")
                            selectedProduct.__setattr__(PRODUCT_COLUMN_NAMES[k],value)

                        printPadding("Modified Product is as follows:")
                        
                        printProductWithBrandName(selectedProduct)

                        answer = getInput('''
                        \rS)ubmit
                        \rC)ancel
                        \rOtherwise, press any key to continue editing''')
                        try:
                            if answer.upper() == 'S':
                                editing = False
                            if answer.upper() == 'C':
                                editing = False
                                raise Exception("Cancelling...")
                        except:
                            getInput("Rolling Back Changes")
                            
                    try:
                        session.commit()
                        printPadding('Product updated successfully')
                        viewing = False
                    except:
                        session.rollback()
                        print("Commit Failed: Rolling Back Changes")

                if editSelection == "D":
                    deleting = True
                    while deleting:
                        try:
                            answer = getInput("Are you sure you want to delete product?").upper()
                            if answer in DELETE_OPTIONS:
                                if answer == 'Y':
                                    session.delete(selectedProduct)
                                deleting = False
                                editing = False
                            else:
                                raise Exception
                        except:
                            printPadding("Please Enter Y or N")
                if editSelection == "P":
                    break
            else:
                printPadding("Please Enter either E, D, or P")

def format_price(price):
    try:
        price = float(price)
        return price
    except TypeError:
        printPadding("TypeError")
    except ValueError:
        printPadding("ValueError")
def format_date(date, selectedProduct):
    dateArray = date.split('-')
    dateDate = datetime.date(int(dateArray[0]),int(dateArray[1]),int(dateArray[2]))
    if(selectedProduct.date_updated):
        if(dateDate >= selectedProduct.date_updated):
            return dateDate
        elif(dateDate < selectedProduct.date_updated):
            raise ValueError("New date is older than existing date")
    else:
        return dateDate
def new_product():
    addingNew = True
    while addingNew:
        newProduct = Product()
        for i, v in enumerate(PRODUCT_COLUMNS_ALIASED):
            if(i != 0):        
                if PRODUCT_COLUMNS_ALIASED[i] == 'Product Price':
                    value = getInput(f"{v}: ")
                    try:
                        value = format_price(value)
                    except TypeError as e:
                        getInput(e)
                    except ValueError as e:
                        getInput(e)
                    else:
                        newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)
                elif PRODUCT_COLUMNS_ALIASED[i] == 'Date Updated':
                    value = date.today()
                    try:
                        newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)
                    except ValueError as e:
                        getInput(e)      
                elif PRODUCT_COLUMNS_ALIASED[i] == 'Brand Name':
                    brandName = getInput(f"{v}: ")
                    searchedBrand = session.query(Brand).filter(Brand.brand_name == brandName).one_or_none()
                    if(searchedBrand):
                        newProduct.brand_id = searchedBrand.brand_id
                    else:
                        brand = Brand()
                        brand.brand_name = brandName
                        session.add(brand)
                        addedBrand = session.query(Brand).filter(Brand.brand_name == brandName).one()
                        newProduct.brand_id = addedBrand.brand_id

                else:
                    value = getInput(f"{v}: ")
                    newProduct.__setattr__(PRODUCT_COLUMN_NAMES[i], value)

        try:
            queriedProduct = session.query(Product).filter(Product.product_name == newProduct.product_name).one_or_none()
            if(queriedProduct):
                queriedProduct.product_price = newProduct.product_price
                queriedProduct.product_quantity = newProduct.product_quantity
                queriedProduct.date_updated = newProduct.date_updated
                queriedProduct.brand_id = newProduct.brand_id
                session.commit()
                addingNew = False
            else:
                session.add(newProduct)
                session.commit()
                printPadding(f'{newProduct} updated successfully')
                addingNew = False      
            
        except IntegrityError as e:
            getInput(e)
            session.rollback()
            printPadding("Commit Failure.  Rolling Back Changes")

def _get_product():
    read_input = getInputInt("Enter Product Id: ")
    try:
        return session.query(Product).join(Brand).filter(Product.product_id == read_input).one()
    except NoResultFound as e:
        getInput(e)
    except MultipleResultsFound as e:
        getInput(e)

def analyse_products():
    analyzing = True
    while analyzing:
        printPadding('ANALYSIS MENU: ')
        for i, v in enumerate(ANALYSIS_OPTIONS):
           print(f'{i+1}: {v}')
        itsANumber = getInputInt("?: ")
        
        if itsANumber == 1:
            printProductWithBrandName(session.query(Product).order_by(Product.product_price.desc()).first())
        elif itsANumber == 2:
            printProductWithBrandName(session.query(Product).order_by(Product.product_price).first())
        elif itsANumber == 3:
            productBrands = session.query(Product).join(Brand).all()
            brandCounts = {}
            mostPopularBrand = 'V8'
            for each in productBrands:
                brandName = each.__getattribute__('brands.brand_id').__getattribute__('brand_name')
                if(brandName in brandCounts):
                    brandCounts[brandName] += 1
                else:
                    brandCounts[brandName] = 1
            for k,v in brandCounts.items():
                if brandCounts[k] > brandCounts[mostPopularBrand]:
                    mostPopularBrand = k
            print(f'Top Brand: {mostPopularBrand} with {brandCounts[mostPopularBrand]} items')
        elif itsANumber == 4:
            printProductWithBrandName(session.query(Product).order_by(Product.date_updated.desc()).first())
        elif itsANumber == 5:
            printProductWithBrandName(session.query(Product).order_by(Product.date_updated).first())
        elif itsANumber == 6:
            printProductWithBrandName(session.query(Product).order_by(Product.product_quantity.desc()).first())

        answer = getInput('To quit press Q. Otherwise, press any key to continue')

        if answer == 'Q':
            analyzing = False
    
def backup_database():
    productBrands = session.query(Product).join(Brand).all()
    try:
        with open('backup_inventory.csv', 'w', newline='') as csvfile:
            rowWriter = csv.writer(csvfile, delimiter=',')
            rowWriter.writerow(PRODUCT_BRAND_CSV_COLUMN_NAMES)
            for v in productBrands:
                brandName = v.__getattribute__('brands.brand_id').__getattribute__('brand_name')
                dateString = v.date_updated.isoformat()
                dateArray = dateString.split("-")
                rowWriter.writerow([v.product_name,f"${v.product_price}",v.product_quantity,f"{dateArray[1]}/{dateArray[2]}/{dateArray[0]}", brandName])
        
        printPadding("Inventory database backed up")
        csvfile.close()
        
    except:
         getInput("Exception on Inventory Database Export")
    brands = session.query(Brand).all()
    try:
        with open('backup_brands.csv', 'w', newline='\n') as csvfile2:
            rowWriter = csv.writer(csvfile2)
            for v in brands:
                rowWriter.writerow([v.brand_name])
        
        printPadding("Brand database backed up")
        
    except:
         getInput("Exception on Brands Database Export")
    
