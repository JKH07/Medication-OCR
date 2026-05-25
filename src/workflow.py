from src.ocr import perform_OCR
from src.save_to_data_base import insert_medication
from src.validation import validate

def pipeline(image):
    data=ocr_exctraction(image)
    if(data):
        
        return validate_medication(data)
        
    else:
        return "didnt work"
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
# def save(data:dict):
#     #try exc block inside
#     insert_medication(data)



