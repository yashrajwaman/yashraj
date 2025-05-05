import streamlit as st
import hashlib
import json

# Function to create a hash of the ticket entry
def generate_hash(entry):
    entry_str = json.dumps(entry, sort_keys=True)
    return hashlib.sha256(entry_str.encode()).hexdigest()

# Initialize session state for the ledger
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

st.title("🎟️ Ticket Selling System with Hashing")

st.header("Sell a Ticket")
with st.form("ticket_form"):
    event = st.text_input("Event Name")
    ticket_id = st.text_input("Ticket ID")
    buyer = st.text_input("Buyer Name")
    price = st.number_input("Price", min_value=0.0, step=1.0)
    submit = st.form_submit_button("Sell Ticket")

    if submit:
        # Check for duplicate ticket ID
        if any(entry['Ticket ID'] == ticket_id for entry in st.session_state.ledger):
            st.error(f"Ticket ID '{ticket_id}' already sold!")
        else:
            entry = {
                'Event': event,
                'Ticket ID': ticket_id,
                'Buyer': buyer,
                'Price': price
            }
            entry['Hash'] = generate_hash(entry)
            st.session_state.ledger.append(entry)
            st.success(f"Ticket {ticket_id} sold to {buyer} for ${price:.2f}.")

st.header("📒 Ticket Sale Ledger")
if st.session_state.ledger:
    st.dataframe(st.session_state.ledger)
else:
    st.info("No tickets sold yet.")
