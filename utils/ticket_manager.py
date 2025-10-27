import json
import os

TICKETS_FILE = "tickets.json"

if not os.path.exists(TICKETS_FILE):
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def load_tickets():
    with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tickets(tickets):
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

def add_ticket(user_id, question, answer):
    tickets = load_tickets()
    user_tickets = tickets.get(str(user_id), [])
    user_tickets.append({"question": question, "answer": answer})
    tickets[str(user_id)] = user_tickets
    save_tickets(tickets)

def delete_ticket(user_id, index):
    tickets = load_tickets()
    if str(user_id) in tickets and 0 <= index < len(tickets[str(user_id)]):
        del tickets[str(user_id)][index]
        save_tickets(tickets)
        return True
    return False

def get_tickets(user_id):
    tickets = load_tickets()
    return tickets.get(str(user_id), [])
