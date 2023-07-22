from flask import Flask, render_template, request

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/split', methods=['POST'])
def split():
    form_data = request.form
    print(form_data)

    for key, value in form_data.items():
        print(f"{key}: {value}")

    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)