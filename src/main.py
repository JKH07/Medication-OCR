from workflow import pipeline

def main(data):
    try:
        pipeline(data)
        print("Success! Saved.")
    except Exception as err:
        print(err)
