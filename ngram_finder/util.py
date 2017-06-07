class DoublespaceLineCorpus:    
    def __init__(self, corpus_fname, num_doc = -1, num_sent = -1, iter_sent = False, skip_header = 0):
        self.corpus_fname = corpus_fname
        self.num_doc = 0
        self.num_sent = 0
        self.iter_sent = iter_sent
        self.skip_header = skip_header
        if (num_doc > 0) or (num_sent > 0):
            self.num_doc, self.num_sent = self._check_length(num_doc, num_sent)

    def _check_length(self, num_doc, num_sent):
        num_sent_ = 0
        with open(self.corpus_fname, encoding='utf-8') as f:
            for _ in range(self.skip_header):
                next(f)
            for doc_idx, doc in enumerate(f):
                if (num_doc > 0) and (doc_idx >= num_doc):
                    return doc_idx, num_sent_
                sents = doc.split('  ')
                sents = [sent for sent in sents if sent.strip()]
                num_sent_ += len(sents)
                if (num_sent > 0) and (num_sent_ > num_sent):
                    return doc_idx, min(num_sent, num_sent_)
        return doc_idx+1, num_sent_
            
    def __iter__(self):
        with open(self.corpus_fname, encoding='utf-8') as f:
            for _ in range(self.skip_header):
                next(f)
            num_sent = 0
            stop = False
            for doc_idx, doc in enumerate(f):
                if stop:
                    break
                if not self.iter_sent:
                    yield doc.strip()
                    if (self.num_doc > 0) and ((doc_idx + 1) >= self.num_doc):
                        stop = True
                    continue
                for sent in doc.split('  '):
                    num_sent += 1
                    if (self.num_sent > 0) and (num_sent > self.num_sent):
                        stop = True
                        break
                    sent = sent.strip()
                    if not sent: continue
                    yield sent.strip()
                    
    def __len__(self):
        if self.num_doc == 0:
            self.num_doc, self.num_sent = self._check_length(-1, -1)
        return self.num_sent if self.iter_sent else self.num_doc