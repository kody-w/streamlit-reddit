import json
import streamlit as st
from google.oauth2 import service_account
from google.cloud import firestore

# Load credentials and initialize Firestore client
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit-22078")

st.header('Hello 🌎! Welcome to the Best List of ChatGPT Prompts to Use')


# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
description = st.text_area("Post description", height=200)
submit = st.button("Submit new post")
if st.button('Balloons?'):
    st.balloons()

# Submit new post to the database
if title and url and description and submit:
    doc_ref = db.collection("posts").document(title)
    doc_ref.set({
        "title": title,
        "url": url,
        "description": description,
        "upvotes": 0
    })

# Retrieve and render posts sorted by upvotes
posts_ref = db.collection("posts").order_by("upvotes", direction=firestore.Query.DESCENDING)
for doc in posts_ref.stream():
    post = doc.to_dict()
    title = post["title"]
    url = post["url"]
    description = post.get("description", "")  # Use get() method with a default value
    upvotes = post["upvotes"]

    st.subheader(f"Post: {title}")
    st.write(f":link: [{url}]({url})")
    if description:
        st.markdown(description)
    st.write(f":thumbsup: Upvotes: {upvotes}")

    # Upvote button
    upvote_button = st.button(f"Upvote {title}")
    if upvote_button:
        # Increment upvotes and update the post in the database
        post_ref = db.collection("posts").document(title)
        post_ref.update({"upvotes": firestore.Increment(1)})
        st.experimental_rerun()
