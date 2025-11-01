from fastapi import FastAPI , Body, HTTPException, Query

app = FastAPI()

USERS = {
    1:{"fname":"a" , "lname":"b" , "age":1},
    2:{"fname":"c" , "lname":"d" , "age":2},
    3:{"fname":"e" , "lname":"f" , "age":3},
    4:{"fname":"e" , "lname":"f" , "age":3},
    5:{"fname":"e" , "lname":"f" , "age":3}
}

@app.get('/')
async def all_users():
    return USERS    

@app.get("/age")
async def fetch_by_age(age: int = Query(..., description="Age to filter users by")):
    # filter users by age
    result = [
        {"fname": u["fname"], "lname": u["lname"], "age": u["age"]}
        for u in USERS.values()
        if u["age"] == age
    ]
    return result


@app.post('/create_user')
async def create_user(new_user = Body()):
    max_id = max(USERS)
    USERS[max_id+1]=new_user

@app.put('/update_user/{id}')
async def update_user(id : int ,full_update:dict = Body(...)):
    if id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    USERS[id]=full_update
    return {"message": "User updated successfully", "user": USERS[id]}

@app.patch('/patch_user_details/{id}')
async def patch_user_details(id :int , patched_details: dict = Body(..., description="key:val required")):
    if id not in USERS:
        raise HTTPException(status_code=404,detail="not found")
    else:
        USERS[id].update(patched_details)
        return {"message":"done"}   
    
@app.delete('/delete_user/{id}') 
async def delete_user(id : int):
    if id not in USERS.keys():
        raise HTTPException(status_code=400 , detail="not found")
    USERS.pop(id)
    return {"message": f"User {id} deleted successfully"}