from src.workflow import pipeline

def processor(data):
    try:
        return pipeline(data)
        
    except Exception as err:
        return err
