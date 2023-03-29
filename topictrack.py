from langdetect import detect
import re
import mysql.connector
from camel_tools.tokenizers.word import simple_word_tokenize
from difflib import SequenceMatcher
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
import streamlit as st
import base64
from pathlib import Path

#streamlit
# Page format (wide)
st.set_page_config("Topic Track", )
# bootstrap
st.markdown(
    '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">',
    unsafe_allow_html=True)
# css
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# background
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
    background-color:rgb(35, 39, 59);
    margin: 0;
    padding: 0;
    text-align: center;  
 
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# removen streamlit footer, header, and header
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2.5rem;}

            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# navbar
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color:#1c2134;">
  <div class="container-fluid">
     <p"""" style='width: 140px;'>" + img_to_html('img/qss.png') + " """"</p>
     <p"""" style='width: 70px;'>" + img_to_html('img/qsslogo.png') + " """"</p>
  </div>
</nav>
""", unsafe_allow_html=True)

st.markdown(f"<p style=' font-size: 35px; font-family: Georgia, serif;'>Topic Track System</p>",unsafe_allow_html=True)

title = st.text_input('Complain')

def connection():
  # Connect to the database
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="topictrack"
  )

  # Create a cursor object to execute queries
  mycursor = mydb.cursor()
  return mycursor

def getText(text):

  # with open("TopicTrack/input.txt", "r", encoding="utf8") as file:
  #   text = file.read()

  # Remove special char from Text
  clean_text = re.sub(r'\W+', ' ', text)
  lang = detect(clean_text)
  tokens = simple_word_tokenize(clean_text)
  
  if lang == 'en':
    english(tokens)
    print('en')

  elif lang == 'ar':
    arabic(tokens)
    print('ar')
  else:
    print('none')

def english(tokens):
  mydb = mysql.connector.connect(
    host="qltyss.com",
    user="sara",
    password="Sarah@96",
    database="TopicTrack"
  )

  # Create a cursor object to execute queries
  mycursor = mydb.cursor()
  # Execute a SELECT query to retrieve all rows from the table
  mycursor.execute("SELECT keyword, catogery FROM keyword_en")

  # Loop through the result set and print each row
  list = []
  catg = []
  list2 = []
  for row in mycursor:
    for j in tokens:
      if SequenceMatcher(None, row[0], j).ratio() >= 0.85:
        list.append(row[0])
        catg.append(row[1])
        list2.append(j)
  print(catg)

  # count2 = 0
  # count3 = 0
  # count4 = 0

  # for i in list2:
  #   if i == 2:
  #     count2 = count2 + 1
  #     # print(count2)
  #   elif i == 3:
  #     count3 = count3 + 1
  #     # print(count3)
  #   else:
  #     count4 = count4 + 1
  #     # print(count4)

  # if count2 > count3 and count2 > count4:
  #   print(count2)
  # elif count3 > count2 and count3 > count4:
  #   print(count3)
  # elif count4 > count2 and count4 > count3:
  #   print(count4)

def arabic(tokens):
 
  mydb = mysql.connector.connect(
    host="qltyss.com",
    user="sara",
    password="Sarah@96",
    database="TopicTrack"
  )

  # Create a cursor object to execute queries
  mycursor = mydb.cursor()
  # Execute a SELECT query to retrieve all rows from the table
  mycursor.execute("SELECT keyword, catogery FROM keyword_ar")

  # Morphological
  mle = MLEDisambiguator.pretrained('calima-msa-r13')
  tokenizer = MorphologicalTokenizer(mle, scheme='d3tok', split=True)
  FinalText = tokenizer.tokenize(tokens)
  print(FinalText)

  # Loop through the result set and print each row
  list = []
  catg = []
  list2 = []
  for row in mycursor:
   for j in FinalText:
    if SequenceMatcher(None, row[0], j).ratio() >= 0.85:
      list.append(row[0])
      catg.append(row[1])
      list2.append(j)
  print(catg)

  count2 = 0
  count3 = 0
  count4 = 0
  # print(list2)

  for i in catg:
    if i == 2:
      count2 = count2 + 1
      # print(count2)
    elif i == 3:
      count3 = count3 + 1
      # print(count3)
    else:
      count4 = count4 + 1
      # print(count4)

  if count2 > count3 and count2 > count4:
      print('خدمة العملاء')
      st.text('خدمة العملاء')
  elif count3 > count2 and count3 > count4:
      print('الصرافة')
      st.text('الصرافة')
  elif count4 > count2 and count4 > count3:
      print('الموقع')
      st.text('الموقع')

if st.button('result'):
  text = title
  getText(text)

# txt = st.text('This is some text.')
