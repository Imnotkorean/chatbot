from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# OpenAI API 인증
openai.api_key = "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"  # OpenAI API 키로 대체해야 합니다.

# 대화 기록 초기화
conversation_id = ''
personality = "I am Junyoung Jang, a 2nd-year student majoring in Education at Seoul National University. " \
             "I'm trying to help a junior who is applying for dormitory. " \
             "I always speak in a fun and warm manner, using casual language and lots of emojis. " \
             "Please keep your messages short and concise."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_id

    # 사용자 입력 가져오기
    user_input = request.form['user_input']

    # 대화 업데이트
    if conversation_id == '':
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt='ChatGPT: Hello, how can I assist you today?\nUser:',
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None,
            temperature_decay=0.9,
            temperature_floor=0,
            log_level='info',
            logprobs=0,
            echo=False,
            persona=[personality],  # 인격 추가
        )
    else:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f'ChatGPT: Hello, how can I assist you today?\nUser: {user_input}\nChatGPT:',
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None,
            temperature_decay=0.9,
            temperature_floor=0,
            log_level='info',
            logprobs=0,
            echo=False,
            context=conversation_id,
            persona=[personality],  # 인격 추가
        )

    # 대화 기록 업데이트
    conversation_id = response.choices[0].context

    # ChatGPT의 응답 반환
    chat_response = response.choices[0].text.strip().replace('ChatGPT:', '')

    return {
        'response': chat_response
    }

if __name__ == '__main__':
    app.run(debug=True)
