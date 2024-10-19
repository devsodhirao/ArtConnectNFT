import uuid

def mint_token(user_id, artwork_title):
    # Simulate minting a new token
    token_id = str(uuid.uuid4())
    print(f"Minted token {token_id} for user {user_id}: {artwork_title}")
    return token_id

def transfer_token(token_id, from_user_id, to_user_id):
    # Simulate transferring a token
    print(f"Transferred token {token_id} from user {from_user_id} to user {to_user_id}")
    return True

def get_token_owner(token_id):
    # Simulate getting the owner of a token
    # In a real blockchain, this would query the current state
    print(f"Querying owner of token {token_id}")
    return "simulated_owner_id"
