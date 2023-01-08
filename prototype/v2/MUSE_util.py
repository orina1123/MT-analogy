# from: https://colab.research.google.com/drive/1fYrIK1mQsksnxnoiwwsuIcgAHIpT-CCI?usp=sharing

def word_most_similar_same_emb(emb, word, n=10):
  if word not in emb:
    return None
  return emb.most_similar(positive=[word], topn=n)

def src_word_most_similar_in_tgt(src_emb, tgt_emb, src_word, n=10):
  if src_word not in src_emb:
    return None
  return tgt_emb.most_similar(positive=[ src_emb[src_word] ], topn=n)

def src_word_least_similar_in_tgt(src_emb, tgt_emb, src_word, n=10):
  if src_word not in src_emb:
    return None
  least_sim_list = tgt_emb.most_similar(positive=[ src_emb[src_word] ], topn=1000)[-n:]
  least_sim_list.reverse()
  return least_sim_list

def src_word_rank_sim_in_tgt(src_emb, tgt_emb, src_word):
  if src_word not in src_emb:
    return None, None
  for rank, w_sim in enumerate(tgt_emb.most_similar(positive=[ src_emb[src_word] ], topn=100000)):
    tgt_word, sim = w_sim
    if tgt_word == src_word:
      return rank, sim
  # match not found in topn
  return None, None