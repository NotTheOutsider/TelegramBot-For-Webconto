# mongodb+srv://WebC:39K4etkXoX5sMyWC@webcontobot.nwxyn.mongodb.net/?retryWrites=true&w=majority&appName=WebContoBot
# 8097581721:AAFTUl8VXJLYZOeRkxvu0lT3KRD9IsN8580
# 1086125120
import uvicorn
from routers import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)