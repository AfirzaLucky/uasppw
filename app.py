import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer

Data, lda, Model, Implementasi = st.tabs(['Data', 'LDA', 'Modelling', 'Implementasi'])
#https://github.com/AfirzaLucky/uasppw
with Data:
   st.title("Impelementasi Latent Dirichlet Allocation (LDA) ")
   st.text("Afirza Lucky Pradana - 210411100018")
   st.subheader("Deskripsi Data")
   st.write("Fitur Fitur yang ada diantaranya:")
   st.text("Fitur-fitur data:")
   st.text("1) Judul")
   st.text("2) Isi")
   st.text("3) Label")
   st.subheader("Data")
   data = pd.read_csv("berita.csv")
   st.write(data)

with lda:
   topik = st.number_input("Masukkan Jumlah Topik yang Diinginkan", 1, step=1, value=5)
   lda_model = None  # Inisialisasi lda_model

   def submit():
      tf = pd.read_csv("df_tf.csv")
      lda = LatentDirichletAllocation(n_components=topik, doc_topic_prior=0.2, topic_word_prior=0.1, random_state=42, max_iter=1)
      lda_top = lda.fit_transform(tf)
      # Bobot setiap topik terhadap dokumen
      nama_clm = [f"Topik {i+1}" for i in range(topik)]
      U = pd.DataFrame(lda_top, columns=nama_clm)
      data_with_lda = pd.concat([U, data['Label']], axis=1)
      st.write(data_with_lda)

   all = st.button("Submit")
   if all:
      submit() 

with Model:
    tf = pd.read_csv("dftf.csv")
    st.subheader("Jumlah Topik yang Anda Gunakan : " + str(topik))
    st.write("Jika pada menu LDA tidak menentukan jumlah topiknya maka proses modelling akan di default dengan jumlah topik = 5")
    lda = LatentDirichletAllocation(n_components=topik, doc_topic_prior=0.2, topic_word_prior=0.1, random_state=42, max_iter=1)
    lda_top = lda.fit_transform(tf)
    # Bobot setiap topik terhadap dokumen
    nama_clm = [f"Topik {i+1}" for i in range(topik)]
    U = pd.DataFrame(lda_top, columns=nama_clm)
    data_with_lda = pd.concat([U, data['Label']], axis=1)
   
    df = data_with_lda.dropna(subset=['Label', 'Label'])

    X = df.drop(columns=['Label']).values
    y = df['Label'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Pelatihan model Random Forest dengan data pelatihan
    model1 = RandomForestClassifier(n_estimators=100, random_state=42)
    model1.fit(X_train, y_train)
   
    model2 = MultinomialNB()
    # Pelatihan model Naive Bayes dengan data pelatihan
    model2.fit(X_train, y_train)

    model3 = DecisionTreeClassifier()
    # Pelatihan model Decision Tree dengan data pelatihan
    model3.fit(X_train, y_train)

    st.write("Pilih metode yang ingin anda gunakan :")
    met1 = st.checkbox("Random Forest")
    met2 = st.checkbox("Naive Bayes")
    met3 = st.checkbox("Decision Tree")
    submit2 = st.button("Pilih")

    if submit2:      
        if met1:
            st.write("Metode yang Anda gunakan Adalah Random Forest")
            # Prediksi label kelas pada data pengujian
            y_pred = model1.predict(X_test)
            # Mengukur akurasi model
            accuracy = accuracy_score(y_test, y_pred)
            st.write("Akurasi: {:.2f}%".format(accuracy * 100))
        elif met2:
            st.write("Metode yang Anda gunakan Adalah Naive Bayes")
            # Prediksi label kelas pada data pengujian
            y_pred = model2.predict(X_test)
            # Mengukur akurasi model
            accuracy = accuracy_score(y_test, y_pred)
            st.write("Akurasi: {:.2f}%".format(accuracy * 100))
        elif met3:
            st.write("Metode yang Anda gunakan Adalah Decision Tree")
            # Prediksi label kelas pada data pengujian
            y_pred = model3.predict(X_test)
            # Mengukur akurasi model
            accuracy = accuracy_score(y_test, y_pred)
            st.write("Akurasi: {:.2f}%".format(accuracy * 100))
        else:
            st.write("Anda Belum Memilih Metode")

with Implementasi:
    data = pd.read_csv("berita.csv")
    data['Content'].fillna("", inplace=True)
    count_vectorizer = CountVectorizer(max_df=0.95, min_df=2)
    
    import re

    # Membuat list custom stop words dalam bahasa Indonesia
    custom_stopwords = ["yang", "dan", "di", "dengan", "untuk", "pada", "adalah", "ini", "itu", "atau", "juga"]

    def preprocess_text(text):
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize the text into words (using a simple space-based split)
        words = text.split()
        
        # Remove custom stop words
        words = [word for word in words if word not in custom_stopwords]
        
        # Join the words back into a cleaned text
        cleaned_text = ' '.join(words)
        
        return cleaned_text

    st.subheader("Implementasi")
    st.write("Masukkan Content yang Ingin Dianalisis:")
    user_content = st.text_area("Content", "")

    if user_content:
        # Preproses content
        preprocessed_content = preprocess_text(user_content)

        # Fit vocabulary dengan data latih
        count_vectorizer.fit(data['Content'])

        # Transform abstrak pengguna dengan count_vectorizer
        user_tf = count_vectorizer.transform([preprocessed_content])
       
        if lda_model is None:
            lda_model = LatentDirichletAllocation(n_components=topik, doc_topic_prior=0.2, topic_word_prior=0.1, random_state=42, max_iter=1)
            lda_top = lda_model.fit_transform(user_tf)
            st.write("Model LDA telah dilatih.")

        # Transform abstrak pengguna dengan model LDA
        user_topic_distribution = lda_model.transform(user_tf)
        st.write(user_topic_distribution)
        y_pred = model2.predict(user_topic_distribution)
        y_pred

