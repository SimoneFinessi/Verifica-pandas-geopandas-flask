from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

df=pd.read_excel("https://github.com/PolisenoRiccardo/perilPopolo/blob/main/milano_housing_02_2_23.xlsx?raw=true")
@app.route('/')
def home():
    return render_template("home.html")

@app.route("/varianti")
def var():
    lista=df["neighborhood"].unique()
    return render_template("varianti.html",list=lista)

@app.route('/es1', methods = ["post"])
def es1():
    quar=request.form["quar"]
    trovato=df[df.neighborhood.str.lower()==quar.lower()].sort_values(by=["date"]).to_html()
    return render_template("risultato.html",risultato=trovato) 

@app.route('/es1_v1', methods = ["post"])
def es1_v1():
    quar=request.form.getlist("quar")
    trovato=pd.DataFrame()
    for i in quar:
        ciao=df[df.neighborhood.str.lower()==i.lower()]
        trovato=pd.concat([trovato, ciao])
    trovato=trovato.to_html()
    return render_template("risultato.html",risultato=trovato) 
@app.route('/es1_v2', methods = ["post"])
def es1_v2():
    quar=request.form["quartiere_tendina"]
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
    trovato=df.groupby("neighborhood")[["price"]].mean().sort_values("price").reset_index().to_html()

    return render_template("risultato.html",risultato=trovato) 

@app.route('/es6', methods = ["post"])
def es6():
    def convertitore(a,b):
        for i in range(len(a)):
            a.loc[i,'price']=a.loc[i].price*b
        return a
    TC=int(request.form["TC"])
    trovato=df.groupby("neighborhood")[["price"]].mean().sort_values("price").reset_index()
    media=convertitore(trovato,TC).to_html()
    return render_template("risultato.html",risultato=media) 
if __name__ == '__main__':
    app.run(debug=True)