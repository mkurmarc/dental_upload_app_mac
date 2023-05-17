from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2, config


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
) 

'''make below route async? or not?'''
# returns a JWT token to user if credentials are verified
@router.post("/", response_model=schemas.Token) 
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), 
db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter( # '.username' here because OAuth2PasswordRequestForm  
        models.User.email == user_credentials.username).first() 
                                                                                                             
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id}) #create a token

    return {"access_token": access_token, "token_type": "bearer"} #return token