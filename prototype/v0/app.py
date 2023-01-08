from flask import Flask
from flask import render_template
from flask import Flask, jsonify
import os
#import json
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from MUSE_util import *

app = Flask(__name__)

c_list = [{"name": "-", "text": "Select a community"}, 
    {"name": "psy", "text": "psychology / creativity research"}, 
    {"name": "eng", "text": "engineering / design"}, 
    {"name": "hci", "text": "hci"}, 
    {"name": "mgmt", "text": "management / org science"}
]

print("loading MUSE embeddings ...")

MUSE_emb = {}
for i in range(1, 4+1):
    src = c_list[i]["name"]
    MUSE_emb[src] = {}
    for j in range(1, 4+1):
        if i != j:        
            tgt = c_list[j]["name"]
            MUSE_emb[src][tgt] = {"src_emb": None, "tgt_emb": None}
#TODO load the paths from a file
#MUSE_EXP_BASE_DIR = '/content/drive/MyDrive/OASIS/analogy/s2orc/20200705v1/full/abstract+body_text/MUSE/' # for Colab
MUSE_EXP_BASE_DIR = 'G:/My Drive/OASIS/analogy/s2orc/20200705v1/full/abstract+body_text/MUSE/' # for local

MUSE_emb["psy"]["eng"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community2.sg300/vocab10k/9upqs783wz/vectors-c1.txt')), binary=False)
MUSE_emb["psy"]["eng"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community2.sg300/vocab10k/9upqs783wz/vectors-c2.txt')), binary=False)

MUSE_emb["psy"]["hci"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community3.sg300/vocab5k/o6klwewcam/vectors-c1.txt')), binary=False)
MUSE_emb["psy"]["hci"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community3.sg300/vocab5k/o6klwewcam/vectors-c3.txt')), binary=False)

MUSE_emb["psy"]["mgmt"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community4.sg300/vocab5k/f27qhm93lf/vectors-c1.txt')), binary=False)
MUSE_emb["psy"]["mgmt"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community1.sg300--community4.sg300/vocab5k/f27qhm93lf/vectors-c4.txt')), binary=False)


MUSE_emb["eng"]["psy"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg300--community1.sg300/vocab10k/wbi5o87mzb/vectors-c2.txt')), binary=False)
MUSE_emb["eng"]["psy"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg300--community1.sg300/vocab10k/wbi5o87mzb/vectors-c1.txt')), binary=False)

MUSE_emb["eng"]["hci"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg50i10--community3.sg50i10/vocab7.5k/1g1a21noo6/vectors-c2.txt')), binary=False)
MUSE_emb["eng"]["hci"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg50i10--community3.sg50i10/vocab7.5k/1g1a21noo6/vectors-c3.txt')), binary=False)

MUSE_emb["eng"]["mgmt"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg50i10--community4.sg50i10/vocab7.5k/o77da4r6wq/vectors-c2.txt')), binary=False)
MUSE_emb["eng"]["mgmt"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community2.sg50i10--community4.sg50i10/vocab7.5k/o77da4r6wq/vectors-c4.txt')), binary=False)


MUSE_emb["hci"]["psy"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community1.sg50i10/vocab7.5k/mhz1y46xqm/vectors-c3.txt')), binary=False)
MUSE_emb["hci"]["psy"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community1.sg50i10/vocab7.5k/mhz1y46xqm/vectors-c1.txt')), binary=False)

MUSE_emb["hci"]["eng"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community2.sg50i10/vocab7.5k/roylvnb4gx/vectors-c3.txt')), binary=False)
MUSE_emb["hci"]["eng"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community2.sg50i10/vocab7.5k/roylvnb4gx/vectors-c2.txt')), binary=False)

MUSE_emb["hci"]["mgmt"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community4.sg50i10/vocab7.5k/gfzg4d8vh4/vectors-c3.txt')), binary=False)
MUSE_emb["hci"]["mgmt"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community3.sg50i10--community4.sg50i10/vocab7.5k/gfzg4d8vh4/vectors-c4.txt')), binary=False)


MUSE_emb["mgmt"]["psy"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community1.sg50i10/vocab7.5k/ja9d26hz23/vectors-c4.txt')), binary=False)
MUSE_emb["mgmt"]["psy"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community1.sg50i10/vocab7.5k/ja9d26hz23/vectors-c1.txt')), binary=False)

MUSE_emb["mgmt"]["eng"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community2.sg50i10/vocab7.5k/40jciv4csd/vectors-c4.txt')), binary=False)
MUSE_emb["mgmt"]["eng"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community2.sg50i10/vocab7.5k/40jciv4csd/vectors-c2.txt')), binary=False)

MUSE_emb["mgmt"]["hci"]["src_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community3.sg50i10/vocab7.5k/hn5lvyvxio/vectors-c4.txt')), binary=False)
MUSE_emb["mgmt"]["hci"]["tgt_emb"] = KeyedVectors.load_word2vec_format(datapath(os.path.join(MUSE_EXP_BASE_DIR, 'community4.sg50i10--community3.sg50i10/vocab7.5k/hn5lvyvxio/vectors-c3.txt')), binary=False)

print("MUSE embeddings loaded")

"""
@app.route('/')
def main():
    return render_template("main.html", c_list=c_list)
"""
@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/<filename>')
def root(filename):
    return app.send_static_file(filename)

@app.route('/query/<src>/<tgt>/<word>')
def query(src=None, word=None, tgt=None):
    #return json.dumps({"src": src, "tgt": tgt, "src_word": word})
    src_emb = MUSE_emb[src][tgt]["src_emb"]
    tgt_emb = MUSE_emb[src][tgt]["tgt_emb"]
    
    query_result = {"word": word}
    query_result["src_sim"] = word_most_similar_same_emb(src_emb, word)
    query_result["tgt_sim"] = word_most_similar_same_emb(tgt_emb, word)
    query_result["cross_sim"] = src_word_most_similar_in_tgt(src_emb, tgt_emb, word)
    query_result["self_rank"], query_result["self_sim"] = src_word_rank_sim_in_tgt(src_emb, tgt_emb, word)
    
    return jsonify(query_result)