import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from aiogram.enums import ParseMode
from bot import bot
from db import collection
from helpers import generate_tg_mssg

load_dotenv()

async def send_message_to_chat(params: dict):
    try:
        messageText = generate_tg_mssg(params)

        await bot.send_message(chat_id=os.getenv('CHAT_ID'), text=messageText, parse_mode=ParseMode.MARKDOWN_V2)
        
        await asyncio.to_thread(collection.insert_one, {
            "date":         datetime.now().strftime('%Y-%m-%d, %H:%M:%S'),
            "organisation": params.get('organisation'),
            "user":         params.get('user'),
            "individual":   params.get('individual'),
            "message":      params.get('message'),
            "object":       params.get('object'),
            "tel":          params.get('tel'),
	        "email":        params.get('email'),
	        "release":      params.get('release'),
	        "platform":     params.get('platform'),
            "status":       'waiting for'
        })

        return {"status": "Message sent and saved successfully!"}
    
    except Exception as e:
        return {"error": str(e)}
    
async def get_messages_from_db():
    try:

        docs = await asyncio.to_thread(
            collection.find, {
                'status': 'waiting for'
            }
        )

        result = []
        for doc in docs:
            doc["_id"] = str(doc["_id"])
            result.append(doc)

        return result if result else {"message": "No documents found in the specified range"}

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
    
async def update_messages_from_db():
    try:

        query_filter = {'status' : 'waiting for'}
        update_operation = { '$set' : 
            { 'status' : 'uploaded' }
        }

        result = collection.update_many(query_filter, update_operation)
        
        if result:
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
                }  
        else:
            return {
                "message": "Cannot update status for messages"
                }

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
    
async def rollback_messages_from_db():
    try:

        query_filter = {'status' : 'uploaded'}
        update_operation = { '$set' : 
            { 'status' : 'waiting for' }
        }

        result = collection.update_many(query_filter, update_operation)
        
        if result:
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
                }  
        else:
            return {
                "message": "Cannot update status for messages"
                }

    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
