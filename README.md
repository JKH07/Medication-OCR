# Medication OCR

Allows users to add medications to their profile simply by taking a photo of a medication box or prescription automating the extraction, validation, and storage of medication data without manual input.

---

## Pipeline

| Step | Description | Service |
|------|-------------|---------|
| 1 | Capture image | Frontend |
| 2–3 | Read and process image contents | Gemini API |
| 4 | Structure data into database form | — |
| 5 | Validate medication exists | OpenFDA API |
| 6 | Retrieve active ingredients | RxNorm API |
| 7 | Store in database | Supabase |

> **Why active ingredients?** They are required to determine drug-drug interactions two medications may share an ingredient even if their brand names differ.

---

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python |
| Backend | FastAPI |
| Database | Supabase (PostgreSQL) |
| APIs | Gemini, OpenFDA, RxNorm |

---


