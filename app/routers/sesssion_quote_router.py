from fastapi import APIRouter, Depends, File, Request, Form, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import schemas
from deps import get_session
from .auth_router import get_current_user

session_quote_router = APIRouter(prefix="/session/quote", tags=["session_quote"], dependencies=[Depends(get_current_user)] )

@session_quote_router.post('/create')
async def add_session_quote(session_quote:schemas.SessionQuoteCreate,db:AsyncSession = Depends(get_session)):
    return await crud.create_session_quote(session_quote, db)
@session_quote_router.get('/')
async def get_session_quotes(
        request:Request,
        session_id:int | None = Query(default=None),
        # participant_id:int | None = Query(default=None),
        db:AsyncSession = Depends(get_session)):
    if session_id is None:        
        raise HTTPException(
            status_code=422,  
            detail=[
                {
                    "loc": ["query", "session_id"],
                    "msg": "session_id must be provided",
                    "type": "value_error.missing"
                }
            ]
        )
   
    else:
    #     session_id is not None and participant_id is None:
    #     return await crud.get_session_quotes_by_session_id(session_id, db)
    # elif session_id is not None and participant_id is not None:
        return await crud.get_session_quotes_by_session_user_id(session_id, request.state.user.id, db)
