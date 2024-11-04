from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    from flask import Flask, render_template, request, redirect, url_for

# Database setup
def init_db():
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article1 TEXT NOT NULL,
            article2 TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Sample data: pairs of articles (article1, article2)
article_pairs = [
    ("Article 1 Text Here...", "Article 2 Text Here..."),
    ("Another Article 1 Text...", "Another Article 2 Text..."),
    ("""Assegnata la tutela a Giorgia Righi. Gli altri due pm, Geri Ferrara e il procuratore aggiunto Marzia Sabella, sono già sotto scorta. 18 ottobre 2024 | 10.21 LETTURA: 1 minuto. Il comitato per l'ordine e la sicurezza di Palermo, dopo le minacce ricevute sui social, ha assegnato la tutela alla pm del processo Open Arms Giorgia Righi. Gli altri due pm, Geri Ferrara e il procuratore aggiunto Marzia Sabella, sono già sotto scorta. La campagna diffamatoria sui social e le lettere intimidatorie erano arrivate a settembre dopo la requisitoria al processo Open Arms.
I pm avevano chiesto 6 anni di carcere per Matteo Salvini per avere illegittimamente vietato lo sbarco a Lampedusa a 147 migranti soccorsi in mare dalla nave della Ong spagnola. Le migliaia di messaggi di insulti e minacce indirizzati ai magistrati hanno spinto la procuratrice generale di Palermo Lia Sava a rivolgersi al comitato provinciale per l'ordine e la sicurezza pubblica, l'organo competente ad adottare misure di protezione.
Insulti sessisti, epiteti volgari e lettere anonime inviate in procura generale sono solo alcuni degli episodi segnalati dalla procuratrice generale di Palermo al comitato. Post e minacce sono stati trasmessi anche alla procura di Caltanissetta, competente a indagare nei procedimenti che coinvolgono i magistrati del capoluogo siciliano.

Doctor's Life, formazione continua per i medici. Il primo canale televisivo di formazione e divulgazione scientifica dedicato a Medici di Medicina Generale, Medici Specialisti e Odontoiatri e Farmacisti. Disponibile on demand su SKY.""" , """Arringa dell'avvocata Bongiorno: 'Ong invece di bighellonare doveva andare in Spagna'. In piazza a Palermo manifestazione di solidarietà per il leader della Lega. 18 ottobre 2024 | 11.03 LETTURA: 3 minuti. 'Qui aula bunker del carcere Pagliarelli di Palermo. A testa alta, senza paura, per l'Italia e gli italiani'. Così su X Matteo Salvini, leader della Lega, postando una sua foto, carte alla mano, mentre entra nell'aula del carcere dove oggi si tiene l'arringa difensiva del processo Open Arms, che vede imputato il ministro per sequestro di persona e rifiuto d'atti d'ufficio per non aver fatto sbarcare nell'estate del 2019 i 147 migranti a bordo della nave Open Arms. In piazza esponenti e ministri della Lega per esprimere solidarietà a Salvini.

L'arringa di Bongiorno: 'Si contesta al ministro Salvini il reato di sequestro di persone per avere tenuto dei migranti a bordo, dal 14 al 19 agosto 2019, al contempo si considera legittimo che Open Arms abbia tenuto a bordo gli stessi migranti dal primo al 14 agosto. Quando era evidente a tutti, persino a Malta, che Open Arms aveva il dovere di andare in Spagna', le parole con cui l'avvocata Giulia Bongiorno ha iniziato l'arringa. 'Open Arms ha avuto innumerevoli possibilità di fare sbarcare i migranti ma ha opposto innumerevoli, innumerevoli, innumerevoli rifiuti. Ha scelto di bighellonare anziché andare nel suo Stato di bandiera.

'Dobbiamo uscire dalla logica che è tutto un diritto', ha scandito Bongiorno. 'Una cosa è un diritto, un'altra è la pretesa. Esiste un diritto allo sbarco, non esiste il diritto di scegliere dove e come farli sbarcare e chi fare sbarcare. Mi sono chiesta perché se c'erano tutte queste opzioni hanno scelto di non andare in Spagna'.

In piazza manifestazione di solidarietà per Salvini. In piazza Politeama la manifestazione di solidarietà per Salvini. Un primo piano del leader della Lega e le scritte 'La difesa della patria è un sacro dovere del cittadino' e 'Colpevole di aver difeso l'Italia', sono stampate sulle t-shirt in stile 'wanted' indossate dai parlamentari nazionali, europei e regionali del Carroccio e anche da alcuni militanti del partito, mentre in sottofondo viene trasmessa in diretta l'arringa di Bongiorno. In piazza anche i ministri Giancarlo Giorgetti, Roberto Calderoli e Giuseppe Valditara.

'Sono qui primo perché ero al governo con lui in quel momento e secondo perché sono della Lega come lui', ha detto Giorgetti. 'Io ho legittimo diritto come cittadino a manifestare non contro qualcosa ma a sostegno di Salvini. Sono convinto che la difesa dei confini sia sacra e un dovere e per me Salvini dovrebbe essere premiato, non punito, peggio ancora condannato', ha affermato Calderoli.

Ai cronisti che gli chiedevano dell'opportunità della partecipazione di un ministro alla manifestazione di solidarietà per il leader della Lega, Valditara ha risposto: 'Credo di essere un cittadino libero che va dove ritiene di dovere andare. Manifestare la solidarietà a Matteo Salvini credo sia un atto doveroso per chi crede nella sua politica'.

Assegnata scorta a pm processo Open Arms. Il comitato per l'ordine e la sicurezza di Palermo, dopo le minacce ricevute sui social, ha assegnato la tutela alla pm del processo Open Arms Giorgia Righi. Gli altri due pm, Geri Ferrara e il procuratore aggiunto Marzia Sabella, sono già sotto scorta. La campagna diffamatoria sui social e le lettere intimidatorie erano arrivate a settembre dopo la requisitoria al processo Open Arms.

Demografica, leggi lo Speciale. Persone, popolazione, natalità: Noi domani. Notizie, approfondimenti e analisi sul Paese che cambia."""),
    ("""Assegnata la tutela a Giorgia Righi. Gli altri due pm, Geri Ferrara e il procuratore aggiunto Marzia Sabella, sono già sotto scorta. 18 ottobre 2024 | 10.21 LETTURA: 1 minuto. Il comitato per l'ordine e la sicurezza di Palermo, dopo le minacce ricevute sui social, ha assegnato la tutela alla pm del processo Open Arms Giorgia Righi. Gli altri due pm, Geri Ferrara e il procuratore aggiunto Marzia Sabella, sono già sotto scorta. La campagna diffamatoria sui social e le lettere intimidatorie erano arrivate a settembre dopo la requisitoria al processo Open Arms.

I pm avevano chiesto 6 anni di carcere per Matteo Salvini per avere illegittimamente vietato lo sbarco a Lampedusa a 147 migranti soccorsi in mare dalla nave della Ong spagnola. Le migliaia di messaggi di insulti e minacce indirizzati ai magistrati hanno spinto la procuratrice generale di Palermo Lia Sava a rivolgersi al comitato provinciale per l'ordine e la sicurezza pubblica, l'organo competente ad adottare misure di protezione.

Insulti sessisti, epiteti volgari e lettere anonime inviate in procura generale sono solo alcuni degli episodi segnalati dalla procuratrice generale di Palermo al comitato. Post e minacce sono stati trasmessi anche alla procura di Caltanissetta, competente a indagare nei procedimenti che coinvolgono i magistrati del capoluogo siciliano.

Doctor's Life, formazione continua per i medici. Il primo canale televisivo di formazione e divulgazione scientifica dedicato a Medici di Medicina Generale, Medici Specialisti e Odontoiatri e Farmacisti. Disponibile on demand su SKY.""", """ "Non siamo indeboliti". Poi lo scontro con la mancata consulente. Giorgia Meloni tira dritto e, nel "day after" delle dimissioni di Gennaro Sangiuliano, avverte che il governo non è indebolito ma, anzi, è in piena forma: "Intendo fare il mio lavoro bene fino alla scadenza naturale della legislatura", chiarisce davanti alla platea di Cernobbio, cogliendo anche l'occasione per ringraziare l'ex ministro per il lavoro che ha fatto in questi due anni.

Mentre con una battuta, e senza mai citarla col suo nome, definisce il ruolo di Maria Rosaria Boccia, aprendo uno scontro senza esclusione di colpi con la mancata consulente ministeriale: "Non credo di dovermi mettere a battibeccare con questa persona, lo dico per le tante donne che hanno guardato a questa vicenda come me. La mia idea su come una donna deve guadagnarsi uno spazio nella società è diametralmente opposta da quella di questa persona".

Parole alle quali la diretta interessata replica prima con ironia sui social: "Questa persona è proprio una dilettante!". Poi spiegando le sue convinzioni: "Metta da parte i guantoni, sono la gentilezza e le carezze ciò di cui c'è bisogno", "ogni donna deve essere libera di vivere la propria essenza, nel rispetto degli spazi altrui. Per comprendere appieno gli spazi conquistati, è necessaria l'umiltà di ascoltare la storia con una mente aperta. Solo così possiamo definire quegli spazi fino a raggiungere la dimensione della verità, che apre la possibilità di scegliere consapevolmente e comprendere che ci sono strade diametralmente opposte tra cui scegliere. Tuttavia, ciò che vedo è una donna pronta allo scontro, che affronta la situazione con la forza di un pugile, che soffia il naso dopo il jab, ma non vede di aver sferrato un colpo al vento, senza intaccare la verità", scrive prima di invitare la premier a mettere da parte "i guantoni" """)
    # Add more article pairs as needed
]

@app.route('/')
def survey():
    # Select a random article pair from the list
    article1, article2 = random.choice(article_pairs)  # Randomly select a pair
    return render_template('survey.html', article1=article1, article2=article2)

@app.route('/submit', methods=['POST'])
def submit():
    article1 = request.form['article1']
    article2 = request.form['article2']
    response = request.form['response']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save response to the database
    conn = sqlite3.connect('survey.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO responses (article1, article2, response, timestamp) VALUES (?, ?, ?, ?)',
                   (article1, article2, response, timestamp))
    conn.commit()
    conn.close()
    
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
