from src.workflow import pipeline

def processor(data):
    try:
        pipeline(data)
        return "Success! Saved."
    except Exception as err:
        return err
