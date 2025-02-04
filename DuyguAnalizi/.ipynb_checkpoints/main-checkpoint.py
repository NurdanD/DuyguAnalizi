import streamlit as st

import pandas as pd
import numpy as np
import altair as alt

import joblib

pipe_lr = joblib.load(open("model/duygu_metin.pkl", "rb"))

emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}


def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results


def main():
    st.title("Metin Duygu Algılama")
    st.subheader("Metindeki duyguları algıla")

    with st.form(key='my_form'):
        raw_text = st.text_area("Buraya yazın")
        submit_text = st.form_submit_button(label='Gönder')

    if submit_text:
        col1, col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)

        with col1:
            st.success("Orijinal Metin")
            st.write(raw_text)

            st.success("Tahmin")
            emoji_icon = emotions_emoji_dict[prediction]
            st.write("{}:{}".format(prediction, emoji_icon))
            st.write("Confidence:{}".format(np.max(probability)))

        with col2:
            st.success("Tahmin Olasılığı")
            #st.write(probability)
            proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
            #st.write(proba_df.T)
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["duygular", "olasılık"]

            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='duygular', y='olasılık', color='duygular')
            st.altair_chart(fig, use_container_width=True)






if __name__ == '__main__':
    main()