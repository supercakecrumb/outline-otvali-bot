from models.db_models import Client, Server, client_server_association, init_db

Session = init_db("sqlite:///app.db")

def add_client(session, tg_id, username, is_approved=True):
    new_client = Client(tg_id, username)
    new_client.is_approved = True
    session.add(new_client)
    session.commit()

def add_server(session, api_url, cert_sha256, country, city, num_users):
    new_server = Server(api_url=api_url, cert_sha256=cert_sha256, country=country, city=city, num_users=num_users)
    session.add(new_server)
    session.commit()

def approve_client(session, client_id):
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        client.is_approved = True
        session.commit()

def delete_client(session, client_id):
    client = session.query(Client).filter_by(id=client_id).first()
    if client:
        session.delete(client)
        session.commit()

def delete_server(session, server_id):
    server = session.query(Server).filter_by(id=server_id).first()
    if server:
        session.delete(server)
        session.commit()

def associate_client_server(session, client_id, server_id, outline_id):
    session.execute(client_server_association.insert().values(client_id=client_id, server_id=server_id, outline_id=outline_id))
    session.commit()

# Example of usage
if __name__ == "__main__":
    session = Session()
    add_server(session, "https://164.92.161.84:23870/PwAYn7W0w_jIRXJFCOQAiw", "A8958F76CEC98DCF5EE6D0C6F89785ECF169E4211686AA9DCCE10F4E16514B00", "Germany", "Frankfurt", 0)
    add_client(session, 123, "username", is_approved=True)
    # add_client(session, 1, "john_doe")
    # add_server(session, "https://example.com", "cert_sha256_here", "192.168.1.1", 5000, "US", "San Francisco", 0)
    # approve_client(session, 1)
    # associate_client_server(session, 1, 1)