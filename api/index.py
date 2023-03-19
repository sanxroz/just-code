from flask import Flask, render_template, request, jsonify
import requests
import openai

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/submit', methods=['POST'])
def submit():

    open_ai_cookie = request.cookies.get("not-api-cookie")

    if not open_ai_cookie:
        return jsonify({'message': 'No OpenAI key, check https://platform.openai.com/account/api-keys for your key'})
    else:
        try:
            openai.api_key = f"{open_ai_cookie}"
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a world class coder. Don't explain your response. Don't explain your approach. Don't write anything more than code. Don't explain the code. Only return code. Don't add notes"},
                                                                                       {"role": "user", "content": f"{request.json['inputValue']}. Don't explain your response. Don't explain your approach. Don't write anything more than code. Don't explain the code. Only return code. Don't add notes"}])
            return jsonify({'message': completion.choices[0].message.content})
        except requests.exceptions.RequestException as err:
            print('Something went wrong:', err)
            return jsonify({'message': 'Something went wrong'}), 500


if __name__ == '__main__':
    app.run(debug=True)
