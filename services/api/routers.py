from fastapi import FastAPI, HTTPException
import services.common.exceptions as exceptions
import services.api.controllers as controllers

app = FastAPI()
app.add_exception_handler(HTTPException, exceptions.http_exception_handler)

@app.post('/order') 
async def create_order(params: dict):
    
    org = params.get('organisationID')
    user = params.get('user')
    msg = params.get('message')
    tel = params.get('tel')
    release = params.get('release')
    platform = params.get('platform')

    if not org or not user or not msg or not tel or not release or not platform:
        raise HTTPException(status_code=400, detail="Parameter is required")

    result = await controllers.create_order(params)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@app.get('/order')
async def get_orders():

    result = await controllers.get_orders()
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.patch('/order')
async def update_orders_status(params: dict):
    status = params.get('status')    
    
    if not status:
        raise HTTPException(status_code=400, detail="Parameter is required")

    result = await controllers.update_orders_status()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.post('/verification')
async def submit_verification_code(params: dict):
    code = params.get('code')
    
    if not code:
        raise HTTPException(status_code=400, detail="Parameter is required")
    
    result = await controllers.submit_verification(code)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.post('/answear')
async def send_answear(params: dict):
    userID = params.get('userID')
    answ = params.get('answear')    
    
    if not userID or not answ:
        raise HTTPException(status_code=400, detail="Parameter is required")

    result = await controllers.send_answear(params)
    
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