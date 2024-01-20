from flask import Flask,flash
from FinancialLines.app import financiallines
from flask_caching import Cache


app = Flask(__name__)

app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = '.'  
cache = Cache(app)

# Path todo
app.register_blueprint(financiallines,url_prefix='/financiallines')

if __name__ == '__main__':
    app.run(debug=True)
