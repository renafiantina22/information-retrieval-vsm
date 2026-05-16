# Laporan Penugasan
---

## Cara Menjalankan Program

1. install Library NLTK yang diperlukan menggunakan perintah "pip install -r requirements.txt"
2. Memastikan data-data yang akan diinputkan berada dalam satu folder yang sama dengan vsm.py
3. Untuk menjalankan program dapar menggunakan perintah python vsm.py base.txt query.txt
4. Memastikan hasil (output) dengan membuka index.txt, wights.txt dan response.txt

---

## Algoritma yang digunakan 

1. Preprocessing 
Dokumen dan query diproses terlebih dahulu menggunakan tahapan - tahapan berikut: 
- Lowercase
- Tokenisasi
- Stopword
- Stemming

2. Term Frequency (TF)
TF digunakan untuk menghitung frekuensi kemunculan suatu term pada dokumen. Semakin sering suatu tem muncul, maka bobot TF akan semakin besar.  
Rumus yang digunakan :
TF = 1 + log (freq)

3. Inverse Document Frequency (IDF)
IDF digunakan untuk mengukur tingkat kepentingan suatu term berdasarkan jumlah dokumen yang mengandung term tersebut. Term yang jarang muncul pada dokumen lain akan memiliki nilai IDF lebih besar.

Rumus yang digunakan:
IDF = log(N / n)

4. TF - IDF 
TF-IDF digunakan untuk merepresentasikan dokumen dan query dalam bentuk vector. Bobot akhir setiap term dihitung menggunakan TF-IDF.
Rumus:
TF-IDF = TF × IDF

5. Cosine Similarity
Cosine similarity digunakan untuk menghitung tingkat kemiripan antara query dan dokumen berdasarkan vector TF-IDF. Dokumen dengan nilai cosine similarity lebih besar dianggap lebih relevan terhadap query.
Rumus:
cos(θ) = (d · q) / (||d|| ||q||)

6. Ranking Dokumen
Setelah nilai similarity dihitung, dokumen diurutkan dari nilai similarity terbesar ke terkecil. Dokumen dengan similarity tertinggi akan berada pada urutan pertama hasil pencarian.

---

## Contoh hasil keluaran

```txt
Base file: base.txt
Query file: query3.txt

Isi query:
football tournament player goal
['doc1.txt', 'doc2.txt', 'doc3.txt', 'doc4.txt', 'doc5.txt']

Processed Query:
['footbal', 'tournament', 'player', 'goal']

Query TF:
{'footbal': 1.0, 'tournament': 1.0, 'player': 1.0, 'goal': 1.0}

Query TF-IDF:
{'footbal': 1.6094379124341003, 'tournament': 1.6094379124341003, 'player': 1.6094379124341003, 'goal': 1.6094379124341003}

Cosine Similarity:
doc1.txt : 0.0000
doc2.txt : 0.0000
doc3.txt : 0.0000
doc4.txt : 0.0000
doc5.txt : 0.6229

Ranking Dokumen:
1. doc5.txt -> 0.6229
2. doc1.txt -> 0.0000
3. doc2.txt -> 0.0000
4. doc3.txt -> 0.0000
5. doc4.txt -> 0.0000
```

Hasil tersebut menunjukkan bahwa `doc3.txt` merupakan dokumen yang paling relevan terhadap query karena memiliki nilai cosine similarity tertinggi.