import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO

def summarize_llm(text):
    import time
    from openai import OpenAI

    ASSISTANT_ID = "asst_RZqtgyBCFTxJjOf05wKBmHOh"
    client = OpenAI(api_key="")

    #Create a thread with a message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                #Update this with the query you want to use.
                "content": text,
            }
        ]
    )

    #Submit the thread to the assistant.
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"👉 Run Created: {run.id}")

    #Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"🏃 Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f"🏁 Run Completed!")

    #Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    #Return the latest message.
    latest_message = messages[0]
    return latest_message.content[0].text.value


def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


#Streamlit app
def main():
    st.title("Automated Literature Review Generator using LLM 📚🤖")
    st.write(
        "Note: You must insert multiple PDF files all at once. No single PDF should be more than 6 pages. Otherwise, you might get an Error!"
    )

    #Upload multiple PDF files
    uploaded_files = st.file_uploader(
        "Upload PDF files", type="pdf", accept_multiple_files=True
    )

    #Processing uploaded files and generating summaries
    if uploaded_files:
        st.subheader("Literature Review:")
        total_files = len(uploaded_files)
        progress_bar = st.progress(0)
        for i, uploaded_file in enumerate(uploaded_files):
            if i == 0:
                progress_text = st.empty()
            progress_text.text(f"Processing file {i+1} of {total_files}")
            
            text = extract_text_from_pdf(uploaded_file)
    
            summary = summarize_llm(text)
            st.write(summary)
            progress_bar.progress((i + 1) / total_files)
        st.subheader(f"Done!")    

if __name__ == "__main__":
    main()
