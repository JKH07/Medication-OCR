##Medication OCR 
-Allows users to add medications to their profile simply by taking a
photo of a medication box or prescription, automating the extraction, validation, and storage of medication data without manual input.
Pipeline:
1-Picture --> 2-Read Image Contents --> 3-Process Contents Context --> 4-Structure to database column form--> 5-validate medication is real --> 6-get active ingredients--> 7-send to database

1-frontend--> 2/3- Gemini API --> 5-openFDA API --> 6-Rxnorm API --> 7-supabase

Language: Python
Backend: FastAPI
Database: Supabase (PostgreSQL)
APIs: Gemini, OpenFDA, RxNorm

Notes:
- active ingredients are necessary to determine drug-drug interaction
- Images are parsed into a temporary file to access via a file path
