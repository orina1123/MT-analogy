from flask import Flask
from flask import render_template
from flask import Flask, jsonify
import os
#import json
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from MUSE_util import *
from s2_sqlite_util import *
from flask import g

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


@app.route('/')
def index():
    return app.send_static_file("index.html")
"""
@app.route('/v1.number')
def index_number():
    return app.send_static_file("index-number.html")
@app.route('/v1.color')
def index_color():
    return app.send_static_file("index-color.html")
@app.route('/v1.context')
def index_context():
    return app.send_static_file("index-context.html")
"""

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

@app.route('/query-ctx/<src>/<tgt>/<word>')
def query_ctx(src=None, word=None, tgt=None):
    # get MUSE aligned embeddings
    src_emb = MUSE_emb[src][tgt]["src_emb"]
    tgt_emb = MUSE_emb[src][tgt]["tgt_emb"]

    # get sqlite db connection
    con, cur = get_db_con_cur("C:/Users/orina/Downloads/psy+eng+hci+mgmt.in_out_1.s2orc.20200705v1.db")
    """
    con = getattr(g, '_database', None)
    if con is None:
        con, cur = get_db_con_cur()
    else:
        cur = con.cursor()
    """

    query_result = {"word": word, "src_sim": None, "tgt_sim": None}
    src_sim_list = word_most_similar_same_emb(src_emb, word)
    if src_sim_list is None:
        query_result["err_code"] = "NOT_FOUND_IN_SRC_VOCAB"
        query_result["err_msg"] = "query word not found in source vocabulary"
        #return jsonify(query_result)
    else:
        src_res = []
        for w, sim in src_sim_list:     
            #paper_sent_id_list = get_paper_sent_id_contain_word(cur, word, community=src)
            ctx_list = get_ctx_by_word(cur, w, src)
            src_res.append({'word': w, 'sim': sim, 'ctx': process_ctx_list(ctx_list)})
        query_result["src_sim"] = src_res

    tgt_sim_list = word_most_similar_same_emb(tgt_emb, word)
    if tgt_sim_list is None:
        query_result["err_code"] = "NOT_FOUND_IN_TGT_VOCAB"
        query_result["err_msg"] = "query word not found in target vocabulary"
        #return jsonify(query_result)
    else:
        tgt_res = []
        for w, sim in tgt_sim_list:     
            ctx_list = get_ctx_by_word(cur, w, tgt)
            tgt_res.append({'word': w, 'sim': sim, 'ctx': process_ctx_list(ctx_list)})
        query_result["tgt_sim"] = tgt_res

    cross_sim_list = src_word_most_similar_in_tgt(src_emb, tgt_emb, word)
    if cross_sim_list is None:
        pass
    else:
        cross_res = []
        for w, sim in cross_sim_list:     
            ctx_list = get_ctx_by_word(cur, w, tgt)
            cross_res.append({'word': w, 'sim': sim, 'ctx': process_ctx_list(ctx_list)})
        query_result["cross_sim"] = cross_res
        
    query_result["self_rank"], query_result["self_sim"] = src_word_rank_sim_in_tgt(src_emb, tgt_emb, word)
        
    return jsonify(query_result)


def process_ctx_list(ctx_list): #TODO how to choose "most relevant" context for a retrieved word?
    #sent_limit = 2 # at most # sentences per paper, if next paper exists
    #sec_limit = 1 # at most # sentences per section, if next section exists
    #num_paper = 5 
    n_sent_per_paper = 2 # include up to # sentences per paper
    n_ctx_per_word = 5
    ret_ctx_list = []
    sent_cnt = 0
    prev_paper_id = None
    ctx_obj = None
    sent_set = set() #prevent providing same sentences multiple times
    for ctx_row in sorted(ctx_list, key=lambda r: r['paper_id']):
        paper_id = ctx_row['paper_id']
        #print(paper_id, sent_cnt)
        if paper_id == prev_paper_id and sent_cnt >= n_sent_per_paper:
            continue

        if paper_id != prev_paper_id: # reset per-paper counter
            sent_cnt = 0
        
        if ctx_row['sent'] in sent_set:
            continue
        ret_ctx_list.append(ctx_row)
        sent_set.add(ctx_row['sent'])
        sent_cnt += 1
        if len(ret_ctx_list) >= n_ctx_per_word:
            break

        prev_paper_id = paper_id
    #print(ret_ctx_list)
    return ret_ctx_list