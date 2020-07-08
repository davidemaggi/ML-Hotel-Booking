from flask import (
    Flask,
    render_template
)

import connexion

#Creiamo un istanza Flask + Connexion
app = connexion.App(__name__, specification_dir='./')

# Registriamo i dettagli dell'api in swagger
app.add_api('swagger.yml')

# Create a URL route in our application for "/"
@app.route('/')
def home():
   # Mostriamo l'homepage del potale
    return render_template('home.html')

#Laciamo l'app per rispondere a chiamate da qualsiasi IP, sulla porta 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    