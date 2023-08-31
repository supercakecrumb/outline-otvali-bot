from flask import Flask, jsonify, request
from models.db_models import Client, Server, client_server_association  # Assuming you've written this module
from outline_module.outline_vpn.outline_vpn import OutlineVPN  # Adjust the import as necessary
from models.db_models import init_db

Session = init_db('sqlite:///app.db')

app = Flask(__name__)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    client_id = data.get('client_id')
    server_id = data.get('server_id')

    app.logging.debug("wtf?")
    session = Session()

    client_db = session.query(Client).filter_by(id=client_id).first()
    server = session.query(Server).filter_by(id=server_id).first()

    if not client_db or not server:
        return jsonify({"message": "Client or server not found"}), 404

    if not client_db.is_approved:
        return jsonify({"message": "Client is not approved"}), 403

    existing_relation = session.query(client_server_association).filter_by(client_id=client_db.id, server_id=server.id).first()
    
    if existing_relation:
        return jsonify({"message": "User already created on this server"}), 409

    client = OutlineVPN(api_url=server.api_url, cert_sha256=server.cert_sha256)

    new_key = client.create_key()
    session.execute(client_server_association.insert().values(client_id=client_db.id, server_id=server.id, outline_id=new_key.key_id))
    session.commit()

    return jsonify({"message": "User created on the server", "outline_id": new_key.key_id}), 201

@app.route('/delete_user/<string:outline_id>', methods=['DELETE'])
def delete_user(outline_id):
    session = Session()
    client_db = session.query(Client).filter_by(outline_id=outline_id).first()

    if client_db:
        server = client_db.servers[0]  # assuming each client is only associated with one server
        client = OutlineVPN(api_url=server.api_url, cert_sha256=server.cert_sha256)

        client.delete_key(outline_id)  # Deleting from Outline server
        session.delete(client_db)  # Deleting from your database
        session.commit()
        return jsonify({"message": "User deleted"}), 200

    return jsonify({"message": "User not found"}), 404

@app.route('/get_key/<string:outline_id>', methods=['GET'])
def get_key(outline_id):
    session = Session()
    client_db = session.query(Client).filter_by(outline_id=outline_id).first()

    if not client_db:
        return jsonify({"message": "User not found"}), 404

    if not client_db.servers:
        return jsonify({"message": "Client has no relation with any server"}), 403

    server = client_db.servers[0]  # assuming each client is only associated with one server
    client = OutlineVPN(api_url=server.api_url, cert_sha256=server.cert_sha256)

    key_info = [key for key in client.get_keys() if key.key_id == outline_id]

    if key_info:
        return jsonify({"key": key_info[0].access_url}), 200

    return jsonify({"message": "Key not found in the Outline server"}), 404

if __name__ == '__main__':
    app.run(debug=True)
