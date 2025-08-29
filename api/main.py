from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

class InputData(BaseModel):
    data: List[str]

FULL_NAME = "john_doe"
DOB = "17091999"
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"

def is_number(val: str) -> bool:
    return val.isdigit()

def is_alpha(val: str) -> bool:
    return val.isalpha()

def is_special(val: str) -> bool:
    return not (is_number(val) or is_alpha(val))

def alternate_caps(s: str) -> str:
    result = []
    toggle = True
    for ch in reversed(s):
        if toggle:
            result.append(ch.upper())
        else:
            result.append(ch.lower())
        toggle = not toggle
    return "".join(result)

@app.post("/bfhl")
async def process_array(input_data: InputData):
    try:
        data = input_data.data
        
        even_numbers, odd_numbers, alphabets, specials = [], [], [], []
        total_sum = 0

        for item in data:
            if is_number(item):
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                total_sum += num
            elif is_alpha(item):
                alphabets.append(item.upper())
            elif is_special(item):
                specials.append(item)

        concat_str = alternate_caps("".join([ch for ch in data if ch.isalpha()]))

        return {
            "is_success": True,
            "user_id": f"{FULL_NAME.lower()}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": str(total_sum),
            "concat_string": concat_str
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)