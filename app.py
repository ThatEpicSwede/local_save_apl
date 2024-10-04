import json
import streamlit as st
import datetime
import os

# Filnamn för lokal lagring
DATA_FILE = "apl_rapporter.json"
UPLOAD_FOLDER = "uploads"  # Mapp för uppladdade bilder

# Funktion för att läsa data från filen
def read_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Funktion för att skriva data till filen
def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Funktion för att spara uppladdade bilder
def save_image(image_file, week_num):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    image_path = os.path.join(UPLOAD_FOLDER, f"week_{week_num}_{image_file.name}")
    with open(image_path, "wb") as f:
        f.write(image_file.getbuffer())
    return image_path

# Hämta dagens datum och veckonummer
today = datetime.datetime.today()
week_num = today.isocalendar()[1]
formatted_datetime = today.strftime("%Y-%m-%d %H:%M")

def add_entry(title, content, mood, week_num, formatted_datetime, image_path=None):
    data = read_data()
    entry = {
        'week': week_num,
        'timestamp': formatted_datetime,
        'title': title,
        'content': content,
        'mood': mood
    }
    if image_path:
        entry['image'] = image_path
    data.append(entry)
    write_data(data)

def get_entries_by_week(week):
    data = read_data()
    return [item for item in data if item['week'] == int(week)]

st.title('APL-veckorapport')
st.subheader('Lägg till inlägg')
st.write('Fyll i formuläret nedan för att lägga till ett nytt inlägg')

title = st.text_input('Titel')
content = st.text_area(f'Innehåll vecka {week_num}')
mood = st.selectbox('Humör', ["😀", "😭", '😠', '😕', '😐'])
image_file = st.file_uploader("Ladda upp en bild", type=["jpg", "jpeg", "png"])

if st.button('Lägg till'):
    if not title or not content:
        st.error('Titel och innehåll är obligatoriska')
    else:
        image_path = None
        if image_file is not None:
            image_path = save_image(image_file, week_num)
        add_entry(title, content, mood, week_num, formatted_datetime, image_path)
        st.success('Inlägg tillagt!')

def huvudsida():
    st.subheader('Se inlägg')
    # Skapa en lista med tillåtna veckor (38-49, exklusive 44)
    allowed_weeks = [str(week) for week in range(38, 50) if week != 44]
    selected_week = st.selectbox("Välj vecka att visa", allowed_weeks)
    items = get_entries_by_week(int(selected_week))
    if not items:
        st.info(f"Inga inlägg hittades för vecka {selected_week}.")
    else:
        for item in items:
            st.write(f"**Vecka:** {item['week']}")
            st.write(f"**Datum:** {item['timestamp']}")
            st.write(f"**Titel:** {item['title']}")
            st.write(f"**Innehåll:** {item['content']}")
            st.write(f"**Humör:** {item['mood']}")
            if 'image' in item:
                st.image(item['image'], use_column_width=True)
            st.write('---')

def main():
    huvudsida()

if __name__ == "__main__":
    main()
