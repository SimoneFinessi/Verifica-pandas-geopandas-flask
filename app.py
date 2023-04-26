from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

df=pd.read_excel("https://github.com/PolisenoRiccardo/perilPopolo/blob/main/milano_housing_02_2_23.xlsx?raw=true")
@app.route('/')
def home():
    return render_template("home.html")
@app.route('/es1', methods = ["post"])
def es1():
    quar=request.form["quar"]
    trovato=df[df.neighborhood.str.lower()==quar.lower()].sort_values(by=["date"]).to_html()
    return render_template("risultato.html",risultato=trovato) 

@app.route('/es2')
def es2():
    df2=df.dropna(subset=['neighborhood'])
    noRip=list(set(list(df2["neighborhood"])))
    noRip=sorted(noRip)
    return render_template("risultato.html",risultato=noRip) 

@app.route('/es3')
def es3():
    df2=df.dropna(subset=['neighborhood'])
    noRip=df2["neighborhood"].unique()
    noRip=sorted(noRip)
    return render_template("risultato.html",risultato=noRip) 

@app.route('/es4', methods = ["post"])
def es4():
    quar=request.form["zona"]
    zona = df[df["neighborhood"] == quar]["price"].mean()
    return render_template("risultato.html",risultato=zona) 


@app.route('/es5')
def es5():
    noRip=df["neighborhood"].unique()
    media= [df[df["neighborhood"] == i]["price"].mean() for i in noRip]
    media=sorted(media)
    return render_template("risultato.html",risultato=media) 
 
if __name__ == '__main__':
    app.run(debug=True)