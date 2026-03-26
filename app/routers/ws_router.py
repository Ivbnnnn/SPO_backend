from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from websocket_manager import ConnectionManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from .auth_router import get_current_user
from deps import get_session
import schemas, crud, models
from database import AsyncSessionLocal

ws_router = APIRouter(prefix='/ws', tags=['websocket'])
manager = ConnectionManager()

@ws_router.websocket("/session/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id:int,
    ):
    auth: str | None = websocket.headers.get("authorization")
    if not auth or not auth.lower().startswith("bearer "):
        await websocket.close()
        return
    token = auth.split(" ")[1]
    async with AsyncSessionLocal() as db:
        user = await get_current_user(token, db)

        stmt = select(
            exists().where(
                models.Session_Participant.user_id == user.id,
                models.Session_Participant.session_id == session_id
            )
        )

        is_member = await db.scalar(stmt)

        if not is_member:
            await websocket.close()
            return
    await manager.connect(session_id=session_id, websocket=websocket)
    try:
        while True:
            data = await websocket.receive_json()            
            # валидируем и пишем в БД
            msg = schemas.validate_ws_message(data)

            # NOTES

            if msg.type == "note" and msg.data.action_type == 'create':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_note = await crud.create_session_note(note = msg.data.payload, db=db)
                        note_read = schemas.SessionNoteRead.model_validate(db_note)

                        ws_message = schemas.NoteMessageOut(
                            type="note",
                            data=schemas.NoteCreateResponse(
                                action_type="create",
                                payload=note_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "note" and msg.data.action_type == 'update':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_note = await crud.update_session_note(note = msg.data.payload, db=db)
                        note_read = schemas.SessionNoteUpdate.model_validate(db_note)

                        ws_message = schemas.NoteMessageOut(
                            type="note",
                            data=schemas.NoteUpdateData(
                                action_type="update",
                                payload=note_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "note" and msg.data.action_type == 'delete':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_note = await crud.delete_session_note(note = msg.data.payload, db=db)
                        note_read = schemas.SessionNoteDelete.model_validate(db_note)

                        ws_message = schemas.NoteMessageOut(
                            type="note",
                            data=schemas.NoteDeleteData(
                                action_type="delete",
                                payload=note_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })

            # QUOTES

            if msg.type == "quote" and msg.data.action_type == 'create':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_quote = await crud.create_session_quote(quote = msg.data.payload, db=db)
                        quote_read = schemas.SessionQuoteRead.model_validate(db_quote)

                        ws_message = schemas.QuoteMessageOut(
                            type="quote",
                            data=schemas.QuoteCreateResponse(
                                action_type="create",
                                payload=quote_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "quote" and msg.data.action_type == 'update':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_quote = await crud.update_session_quote(quote = msg.data.payload, db=db)
                        quote_read = schemas.SessionQuoteUpdate.model_validate(db_quote)

                        ws_message = schemas.QuoteMessageOut(
                            type="quote",
                            data=schemas.QuoteUpdateData(
                                action_type="update",
                                payload=quote_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "quote" and msg.data.action_type == 'delete':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_quote = await crud.delete_session_quote(quote = msg.data.payload, db=db)
                        quote_read = schemas.SessionQuoteDelete.model_validate(db_quote)

                        ws_message = schemas.QuoteMessageOut(
                            type="quote",
                            data=schemas.QuoteDeleteData(
                                action_type="delete",
                                payload=quote_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })

            # ANSWERS
            if msg.type == "answer" and msg.data.action_type == 'create':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_answer = await crud.create_answer(answer = msg.data.payload, db=db)
                        answer_read = schemas.AnswerRead.model_validate(db_answer)

                        ws_message = schemas.AnswerMessageOut(
                            type="answer",
                            data=schemas.AnswerCreateResponse(
                                action_type="create",
                                payload=answer_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "answer" and msg.data.action_type == 'update':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_answer = await crud.update_session_answer(answer = msg.data.payload, db=db)
                        answer_read = schemas.AnswerUpdate.model_validate(db_answer)

                        ws_message = schemas.AnswerMessageOut(
                            type="answer",
                            data=schemas.AnswerUpdateData(
                                action_type="update",
                                payload=answer_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })
            if msg.type == "answer" and msg.data.action_type == 'delete':
                async with AsyncSessionLocal() as db:
                    try:                        
                        db_answer = await crud.delete_session_answer(answer = msg.data.payload, db=db)
                        answer_read = schemas.AnswerDelete.model_validate(db_answer)

                        ws_message = schemas.AnswerMessageOut(
                            type="answer",
                            data=schemas.AnswerDeleteData(
                                action_type="delete",
                                payload=answer_read 
                            )
                        )
                        await manager.broadcast(session_id=session_id, message=ws_message.model_dump())
                    except Exception as e:
                        await db.rollback()
                        await websocket.send_json({
                            "type":"error",
                            "detail":str(e)
                        })

    except WebSocketDisconnect:
        manager.disconnect(session_id=session_id, websocket=websocket)

