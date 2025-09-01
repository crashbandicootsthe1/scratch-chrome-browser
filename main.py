import scratchattach as sa
import time
import json

# --- Login & connect ---
session = sa.login_by_id("session_id_here", username="crashbandicootsthe1")
cloud = session.connect_cloud("1209832620")  # replace with your project id
client = cloud.requests(respond_order="recieve")

# --- Request handlers ---
@client.request
def ping():
    print("Ping request received")
    return "pong"
    
@client.request()
def save_website(domain, username, site_content):
    website_list = site_content.split("▋")
    with open("websites.json", "r+", encoding="utf-8") as file:
        file_cont = json.load(file)
        domain_json = file_cont.get(domain)
            if domain_json and domain_json.get("owner") == username:
                domain_json["site_content"] = website_list
                file_cont[domain] = domain_json
                file.seek(0)
                file.truncate()
                json.dump(file_cont, file, indent=4, ensure_ascii=False)
                return "Site updated!"
            else:
                return "Access denied."


@client.request()
def load_website(domain):
    with open("websites.json", "r", encoding="utf-8") as file:
        file_cont = json.load(file)

    if domain not in file_cont:
        return "Website does not exist."

    site_content = file_cont[domain].get("site_content")
    if not site_content:
        return "<text>No site content</text>"

    return site_content
        
@client.request
def register_domain(username, domain):
    with open("websites.json", "r+") as file:
        file_cont = json.load(file)
        file_cont[domain] = {
            "owner": username,
            "site_content": ["<text>Hello AttachBrowser!</text>"]
        }
        transaction(username, "crashbandicootsthe1", 12)
        return "Domain registered! Thank you."

BALANCE_FILE = "creditcounts.txt"

def load_balances():
    """Load balances from file into a dictionary."""
    balances = {}
    try:
        with open(BALANCE_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    user, amount = line.strip().split(":")
                    balances[user.strip()] = int(amount.strip())
    except FileNotFoundError:
        pass  # file doesn’t exist yet
    return balances

def save_balances(balances):
    file_path = os.path.abspath(BALANCE_FILE)
    with open(file_path, "w") as f:
        for user, amount in balances.items():
            f.write(f"{user}: {amount}\n")
    print(f"💾 Balances saved to: {file_path}")


@client.request
def register_user(username):
    """Register a new user with 0 balance if not exists."""
    balances = load_balances()
    if username not in balances:
        balances[username] = 25
        save_balances(balances)
        return (f"✅ User '{username}' registered.")
    else:
        return (f"⚠️ User '{username}' already exists.")

@client.request
def get_balance(username):
    """Return balance of a user."""
    balances = load_balances()
    return balances.get(username, None)

@client.request
def transaction(sender, receiver, amount):
    """Transfer money from sender to receiver."""
    balances = load_balances()

    if sender not in balances:
        return f"❌ Sender '{sender}' not found."
    if receiver not in balances:
        return f"❌ Receiver '{receiver}' not found."
    if balances[sender] < amount:
        return f"❌ Not enough funds. {sender} has {balances[sender]}."

    # perform transaction
    balances[sender] -= amount
    balances[receiver] += amount

    save_balances(balances)
    return f"✅ {amount} transferred from {sender} to {receiver}."

# --- Event handlers ---
@client.event
def on_ready():
    print("Request handler is running")

if __name__ == "__main__":
    client.start()
    
    while True:
        time.sleep(5)
