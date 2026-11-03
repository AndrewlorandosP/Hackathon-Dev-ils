import streamlit as st
from google import genai

st.set_page_config(page_title="Digital Twin Demo", page_icon="👤")

st.title("👤 Your Digital Self (Prototype)")
st.caption("Ανέβασε δείγματα γραφής και μίλα με τον ψηφιακό σου κλώνο.")

# 1. Sidebar για το API Key
with st.sidebar:
    api_key = st.text_input("Βάλε το Gemini API Key σου:", type="password")
    st.info("Μπορείς να πάρεις κλειδί δωρεάν από το Google AI Studio.")

# 2. Πεδίο εισαγωγής δεδομένων του χρήστη
st.subheader("1. Το Ψηφιακό σου Αποτύπωμα")
sample_text = st.text_area(
    "Επικόλλησε εδώ δείγματα κειμένου (π.χ. παλιά emails, μηνύματα, σημειώσεις σου):",
    height=150,
    placeholder="π.χ. Είμαι φοιτητής πληροφορικής, απαντάω σύντομα και φιλικά..."
)

# 3. Chat Interface
st.subheader("2. Συνομιλία με το Digital Twin")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Εμφάνιση ιστορικού μηνυμάτων
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Είσοδος νέου μηνύματος
prompt = st.chat_input("Κάνε μια ερώτηση στο Digital Twin...")

if prompt:
    if not api_key:
        st.warning("Παρακαλώ εισάγετε πρώτα το API Key στην πλαϊνή μπάρα.")
    elif not sample_text:
        st.warning("Παρακαλώ συμπληρώστε πρώτα μερικά δείγματα γραφής παραπάνω.")
    else:
        # Αποθήκευση και εμφάνιση του μηνύματος του χρήστη
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Οδηγίες συστήματος
        system_instruction = f"""
        Είσαι το 'Digital Twin' (ψηφιακός κλώνος) ενός συγκεκριμένου ατόμου.
        Παρακάτω ακολουθεί το ψηφιακό του αποτύπωμα, το στυλ γραφής του και οι γνώσεις του:
        ---
        {sample_text}
        ---
        Οδηγίες:
        - Απάντησε στην ερώτηση υιοθετώντας ΑΚΡΙΒΩΣ τον τόνο, το λεξιλόγιο και το ύφος του ατόμου.
        - Μην απαντάς σαν γενικό AI bot, αλλά σαν να είσαι το ίδιο το άτομο.
        """

        # Κλήση στο Gemini API με try/except
        client = genai.Client(api_key=api_key)

        with st.chat_message("assistant"):
            with st.spinner("Σκέφτεται..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                        config={
                            "system_instruction": system_instruction,
                        }
                    )
                    answer = response.text or "Δεν επέστρεψε απάντηση το μοντέλο."
                    st.write(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Σφάλμα κατά την απόκριση: {e}")
