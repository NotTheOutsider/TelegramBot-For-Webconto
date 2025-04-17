from fastapi import FastAPI, HTTPException
import controllers

app = FastAPI()

@app.post('/sendMssgToTG')
async def send_message(params: dict):
    org = params.get('organisation')
    user = params.get('user')
    msg = params.get('message')
    tel = params.get('tel')
    release = params.get('release')
    platform = params.get('platform')

    if not org or not user or not msg or not tel or not release or not platform:
        raise HTTPException(status_code=400, detail="Message parameter is required")

    result = await controllers.send_message_to_chat(params)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.get('/getMssg')
async def get_messages():

    result = await controllers.get_messages_from_db()
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.put('/updateStatus')
async def update_status():

    result = await controllers.update_messages_from_db()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.get('/keepAlive')
async def connection_keep_alive():

    result = {'connection': 'has been extended'}

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result    

# FOR TESTING + 
@app.put('/testRollbackStatus')
async def rollback_status():

    result = await controllers.rollback_messages_from_db()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
# FOR TESTING - 