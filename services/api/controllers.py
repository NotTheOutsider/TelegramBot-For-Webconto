import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from aiogram.enums import ParseMode
from services.bot.bot import bot
from services.common.db import collectionOrders, collectionVerification, collectionChats
from services.common.helpers import generate_tg_mssg, generate_chat_mask

load_dotenv()

async def create_order(params: dict):
    try:
        messageText = generate_tg_mssg(params)

        await bot.send_message(chat_id=os.getenv('CHAT_ID'), text=messageText, parse_mode=ParseMode.MARKDOWN_V2)
        
        await collectionOrders.insert_one({
            "date":             datetime.now().strftime('%Y-%m-%d, %H:%M:%S'),
            "organisation":     params.get('organisation'),
            "organisationID":   params.get('organisationID'),
            "guid":             params.get('guid'),
            "user":             params.get('user'),
            "individual":       params.get('individual'),
            "message":          params.get('message'),
            "object":           params.get('object'),
            "tel":              params.get('tel'),
	        "email":            params.get('email'),
            "telegramMask":     params.get('telegramMask'),
	        "release":          params.get('release'),
	        "platform":         params.get('platform'),
            "status":           'pending'
        })

        return {"status": "Message sent and saved successfully!"}
    
    except Exception as e:
        return {"error": str(e)}
    
async def get_orders():
    try:
        
        # pipeline = [
        #     {
        #         '$lookup': {
        #             'from': 'ChatMasks',
        #             'localField': 'chatMask',
        #             'foreignField': 'chatMask',
        #             'as': 'chatInfo'
        #         }
        #     }
        # ]
        
        result = []
        async for doc in collectionOrders.find({'status': 'pending'}):
            doc["_id"] = str(doc["_id"])
            result.append(doc)
            
        return result if result else {"message": "No documents found in the specified range"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
   
async def update_order_info(params: dict):
    try:
        query_filter = {'guid': params.get("guid")}
        update_operation = {'$set': {
            'date':             datetime.now().strftime('%Y-%m-%d, %H:%M:%S'),
            'organisation':     params.get('organisation'),
            'organisationID':   params.get('organisationID'),
            'guid':             params.get('guid'),
            'user':             params.get('user'),
            'individual':       params.get('individual'),
            'message':          params.get('message'),
            'object':           params.get('object'),
            'tel':              params.get('tel'),
	        'email':            params.get('email'),
            'telegramMask':     params.get('telegramMask'),
	        'release':          params.get('release'),
	        'platform':         params.get('platform'),
            'status': 'pending'
            }}
        result = await collectionOrders.update_many(query_filter, update_operation)
        
        if result:
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }  
        else:
            return {"message": "Cannot update status for messages"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}
    
async def update_orders_status():
    try:
        query_filter = {'status': 'pending'}
        update_operation = {'$set': {'status': 'uploaded'}}
        result = await collectionOrders.update_many(query_filter, update_operation)
        
        if result:
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }  
        else:
            return {"message": "Cannot update status for messages"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}

async def submit_verification(code: str):
    current_time = datetime.now()
    fifteen_minutes_ago = current_time - timedelta(minutes=15)
    try:
        result = await collectionVerification.find_one_and_delete({
            'verification': code,
            'date': {"$gte": fifteen_minutes_ago.strftime('%Y-%m-%d, %H:%M:%S')}
        }) 
    
        if result:
            result["_id"] = str(result["_id"])
            newChatMask = generate_chat_mask()
          
            # Deleting chat if it already exists
            existingChat = await collectionChats.find_one_and_delete({
                'chatID': result['chat']
            })
            
            await collectionChats.insert_one({
                'telegramMask': newChatMask,
                'chatID': result['chat']
            })
            
            return {"telegramMask": newChatMask}
        else:
            return {"message": "No record found matching the criteria"}
    except Exception as e:
        return {"error": str(e)}


async def send_answear(params: dict):
    messageText     = params.get('answear')
    telegramMask    = params.get('telegramMask')
    
    try:
        result = await collectionChats.find_one({'telegramMask': telegramMask});
        
        if not result:
            return {"error": "Can't find chat!"}
        
        await bot.send_message(chat_id=result['chatID'], text=messageText, parse_mode=ParseMode.MARKDOWN_V2,)
        
        return {"status": "Answear sent successfully!"}
    except Exception as e:
        return {"error": str(e)} 

async def rollback_messages_from_db():
    try:
        query_filter = {'status': 'uploaded'}
        update_operation = {'$set': {'status': 'pending'}}
        result = await collectionOrders.update_many(query_filter, update_operation)
        
        if result:
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "acknowledged": result.acknowledged
            }  
        else:
            return {"message": "Cannot update status for messages"}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": str(e)}