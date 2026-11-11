from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# بيانات المثيل الثابتة
ID_INSTANCE = "710722724252"

# جلب الرمز السري بأمان تام من متغيرات البيئة للمنصة (Environment Variables)
API_TOKEN_INSTANCE = os.environ.get("API_TOKEN_INSTANCE")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        
        # التأكد من أن الحدث هو رسالة نصية واردة
        if data.get("typeWebhook") == "incomingMessageReceived":
            sender_data = data.get("senderData", {})
            message_data = data.get("messageData", {})
            
            chat_id = sender_data.get("chatId")
            message_type = message_data.get("typeMessage")
            
            # معالجة الرسائل النصية
            if message_type == "textMessage":
                text = message_data.get("textMessageData", {}).get("textMessage", "")
                print(f"رسالة واردة من {chat_id}: {text}")
                
                # الرد التلقائي للعميل
                welcome_message = "أهلاً بك في شركة أولاد أسوان وأم درمان للشحن 🚚. لقد تلقينا رسالتك وسنرد عليك فوراً!"
                send_whatsapp_message(chat_id, welcome_message)

        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

def send_whatsapp_message(chat_id, message):
    if not API_TOKEN_INSTANCE:
        print("Error: API_TOKEN_INSTANCE is missing!")
        return
        
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
    payload = {
        "chatId": chat_id,
        "message": message
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Send response:", response.text)
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
