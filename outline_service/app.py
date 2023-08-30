from flask import Flask, jsonify, request
from outline_module.outline_handler import OutlineHandler
from models.db_models import Client, Server, Session, client_server_association

app = Flask(__name__)
outline_handler = OutlineHandler()

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    client_id = data.get('client_id')
    server_id = data.get('server_id')

    session = Session()

    # Find the client and server by their IDs
    client = session.query(Client).filter_by(id=client_id).first()
    server = session.query(Server).filter_by(id=server_id).first()

    if not client or not server:
        return jsonify({"message": "Client or server not found"}), 404

    # Check if the client is already associated with the server
    existing_relation = session.query(client_server_association).filter_by(client_id=client.id, server_id=server.id).first()
    
    if existing_relation:
        return jsonify({"message": "User already created on this server"}), 409

    # Create the user on the Outline server
    outline_handler.create_user(client)

    # Add the relationship between client and server, storing the Outline server ID
    session.execute(client_server_association.insert().values(client_id=client.id, server_id=server.id))
    
    session.commit()

    return jsonify({"message": "User created on the server", "outline_id": outline_id}), 201


@app.route('/delete_user/<string:outline_id>', methods=['DELETE'])
def delete_user(outline_id):
    session = Session()
    client = session.query(Client).filter_by(outline_id=outline_id).first()
    if client:
        session.delete(client)
        session.commit()
        outline_handler.delete_user(outline_id)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/get_key/<string:outline_id>', methods=['GET'])
def get_key(outline_id):
    session = Session()
    client = session.query(Client).filter_by(outline_id=outline_id).first()
    if client:
        key = outline_handler.get_key(outline_id)
        return jsonify({"key": key}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
