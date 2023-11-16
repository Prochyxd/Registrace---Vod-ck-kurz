from flask import Flask, jsonify, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')

registrace = [

]
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Spáruje volné uživatele pomocí funkce 'sparte_lidi()'
    Načte index.html stánku
    """
    pary = sparte_lidi()
    return render_template('index.html', registrace=registrace, pary=pary), 200

@app.route('/registrace', methods=['GET', 'POST'])
def druha_stranka():
    """
    Načte registrační stránku
    Získává a kontroluje zadané informace
    """
    if request.method == 'POST':
        je_plavec = request.form['je_plavec']
        nick = request.form['nick']
        kanoe_kamarad = request.form['kanoe_kamarad']

        if je_plavec == '0':
            return jsonify({'status': 'error', 'message': 'Není plavec'}), 400
        
        elif not nick.isalnum() or len(nick) < 2 or len(nick) > 20:
            return jsonify({'status': 'error', 'message': 'Nick není validní'}), 400
        
        elif kanoe_kamarad and (not kanoe_kamarad.isalnum() or len(kanoe_kamarad) < 2 or len(kanoe_kamarad) > 20):
            return jsonify({'status': 'error', 'message': 'Kanoe kamarád není validní'}), 400
        elif nick in [ tmp['nick'] for tmp in registrace]:
            return jsonify({'status': 'error', 'message': 'Uživatel již je zaregistrován'}), 400
        else:
            registrace.append({'nick': nick, 'kanoe_kamarad': kanoe_kamarad})
            return jsonify({'status': 'success', 'message': 'Registrace proběhla úspěšně'}), 200
    return render_template('registrace.html'), 200

def sparte_lidi():
    """
    Spáruje uživatele, kteří nemají kamaráda
    """
    lide_s_kamarady = {r['nick']: r['kanoe_kamarad'] for r in registrace if r['kanoe_kamarad']}
    lide_bez_kamaradu = [r['nick'] for r in registrace if not r['kanoe_kamarad']]

    for nick in lide_bez_kamaradu:
        if nick not in lide_s_kamarady.values():
            volni_lide = [n for n in lide_bez_kamaradu if n != nick]
            if volni_lide:
                vybrany_kamarad = volni_lide[0]
                lide_s_kamarady[nick] = vybrany_kamarad
                lide_bez_kamaradu.remove(vybrany_kamarad)

    return lide_s_kamarady


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
