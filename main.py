from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load data from Excel sheet
xls_path = "/Users/suchithkurra/Desktop/tiger_api/Tiger_data_1.xlsx"
df = pd.read_excel(xls_path)

# Convert float columns to strings to avoid JSON serialization issues
df = df.astype(str)

# Pydantic model for request body
class TigerNameRequest(BaseModel):
    Name: str

# Define API endpoint
@app.post("/get_tiger_by_name/")
async def get_tiger_by_name(request_body: TigerNameRequest):
    try:
        tiger_name = request_body.Name.lower()

        if tiger_name == "tiger":
            # If the user enters "tiger", retrieve all tiger data
            all_tiger_data = df.to_dict(orient="records")
            # Filter out entries with 'Name' column as 'NA' or 'NAN'
            filtered_data = [entry for entry in all_tiger_data if entry.get("Name") and entry["Name"].lower() not in ["na", "nan"]]

            return filtered_data

        # Use iloc to retrieve the row based on the name
        tiger_data = df[df["Name"].str.lower() == tiger_name].to_dict(orient="records")

        if not tiger_data:
            raise HTTPException(status_code=404, detail="Tiger not found")

        # Filter out entries with 'Name' column as 'NA' or 'NAN'
        filtered_data = [entry for entry in tiger_data if entry.get("Name") and entry["Name"].lower() not in ["na", "nan"]]

        return filtered_data[0]  # Assuming there is only one matching tiger
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
