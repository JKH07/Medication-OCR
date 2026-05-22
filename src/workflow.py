from ocr import perform_OCR
from save_to_data_base import insert_medication
from validation import validate

def pipeline(image):
    data=ocr_exctraction(image)
    if(data):
        
        send=validate_medication(data)
        save(send)
    else:
        print("didnt work")
#extract using ocr
def ocr_exctraction(image_path):
    try:
        data=perform_OCR(image_path=image_path)
        print("Sucessful OCR")
        return data
    except Exception as err:
        print(err)
    

#validate using API OPENFDA and add missing data 
def validate_medication(drug_data):
    try:
        found=validate(drug_data)
        return found
    except Exception as err:
        print(err)


# save initial info to database
def save(data:dict):
    #try exc block inside
    insert_medication(data)



