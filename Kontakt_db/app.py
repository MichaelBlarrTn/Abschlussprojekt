import streamlit as st
import sqlite3

# --- Verbindung & Setup ---
def get_connection():
    return sqlite3.connect("kontakte.db", check_same_thread=False)

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    notes TEXT
)
""")
conn.commit()

# --- Hilfsfunktionen ---
def add_contact(name, phone, email, notes):
    cursor.execute("INSERT INTO contacts (name, phone, email, notes) VALUES (?, ?, ?, ?)",
                   (name, phone, email, notes))
    conn.commit()

def get_contacts(search_term=""):
    if search_term:
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                       (f"%{search_term}%", f"%{search_term}%"))
    else:
        cursor.execute("SELECT * FROM contacts")
    return cursor.fetchall()

def update_contact(contact_id, name, phone, email, notes):
    cursor.execute("""UPDATE contacts 
                      SET name=?, phone=?, email=?, notes=? 
                      WHERE id=?""",
                   (name, phone, email, notes, contact_id))
    conn.commit()

def delete_contact(contact_id):
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()

# --- Streamlit UI ---
st.set_page_config(page_title="Kontaktdatenbank", page_icon="📇", layout="centered")
st.title("📇 Kontaktdatenbank mit SQLite")

# --- Kontakt hinzufügen ---
with st.form("add_form"):
    st.subheader("➕ Kontakt hinzufügen")
    name = st.text_input("Name *")
    phone = st.text_input("Telefonnummer")
    email = st.text_input("E-Mail")
    notes = st.text_area("Notizen")
    submitted = st.form_submit_button("Speichern")
    if submitted:
        if name.strip():
            add_contact(name, phone, email, notes)
            st.success(f"Kontakt '{name}' wurde hinzugefügt.")
        else:
            st.error("Name darf nicht leer sein.")

# --- Suche ---
search_term = st.text_input("🔍 Suche nach Name oder Telefonnummer")
contacts = get_contacts(search_term)

# --- Kontaktliste ---
st.subheader("📋 Gespeicherte Kontakte")
if contacts:
    for contact in contacts:
        contact_id, name, phone, email, notes = contact
        with st.expander(f"{name} ({phone if phone else 'keine Nummer'})"):
            st.write(f"**E-Mail:** {email if email else '-'}")
            st.write(f"**Notizen:** {notes if notes else '-'}")

            # Bearbeiten
            with st.form(f"edit_{contact_id}"):
                new_name = st.text_input("Name", value=name)
                new_phone = st.text_input("Telefonnummer", value=phone)
                new_email = st.text_input("E-Mail", value=email)
                new_notes = st.text_area("Notizen", value=notes)
                edit_submitted = st.form_submit_button("💾 Änderungen speichern")
                if edit_submitted:
                    update_contact(contact_id, new_name, new_phone, new_email, new_notes)
                    st.success("Kontakt aktualisiert.")
                    st.experimental_rerun()

            # Löschen
            if st.button("🗑️ Kontakt löschen", key=f"del_{contact_id}"):
                delete_contact(contact_id)
                st.warning("Kontakt gelöscht.")
                st.experimental_rerun()
else:
    st.info("Noch keine Kontakte gespeichert.")
