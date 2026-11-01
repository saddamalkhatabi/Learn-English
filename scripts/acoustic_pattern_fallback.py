"""Acoustic recovery for corrupted Edge-TTS WordBoundary events.
The real recorded MP3 is aligned directly using a pretrained English CTC acoustic
model. Used only when WordBoundary spans are out of order or overlapping.
"""
import pathlib
import re
import numpy as np
import soundfile as sf
import torch
import torchaudio

class ForcedAligner:
    def __init__(self):
        torch.set_num_threads(2)
        self.bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
        self.model=self.bundle.get_model().eval()
        self.labels={letter:i for i,letter in enumerate(self.bundle.get_labels())}

    def align(self, mp3, text):
        words=text.strip().split()
        tokens=[];owners=[]
        for i,word in enumerate(words):
            word="".join(c for c in word.upper() if c in self.labels and c!="|")
            if not word:raise ValueError("No acoustic symbols for a word")
            for c in word:
                tokens.append(self.labels[c]);owners.append(i)
            if i+1<len(words):
                tokens.append(self.labels["|"]);owners.append(-1)
        data,sr=sf.read(pathlib.Path(mp3),dtype="float32")
        if data.ndim>1:data=np.mean(data,axis=1)
        duration=round(len(data)/sr*1000)
        wave=torch.from_numpy(np.ascontiguousarray(data)).unsqueeze(0)
        if sr!=self.bundle.sample_rate:
            wave=torchaudio.functional.resample(wave,sr,self.bundle.sample_rate)
        with torch.inference_mode():
            output,_=self.model(wave)
            emission=output.log_softmax(-1)
            labels=torch.tensor([tokens],dtype=torch.int32)
            aligned,scores=torchaudio.functional.forced_align(emission,labels,blank=self.labels["-"])
            spans=torchaudio.functional.merge_tokens(aligned[0],scores[0],blank=self.labels["-"])
        if len(spans)!=len(tokens):raise ValueError("Incomplete acoustic token spans")
        ms=wave.shape[-1]/emission.shape[1]/self.bundle.sample_rate*1000
        bounds=[[None,None] for _ in words]
        for span,owner in zip(spans,owners):
            if owner<0:continue
            a,b=round(span.start*ms),round(span.end*ms)
            if bounds[owner][0] is None:bounds[owner][0]=a
            bounds[owner][1]=b
        cues=[[i,a,b] for i,(a,b) in enumerate(bounds)]
        if any(a is None or b is None or not (0<=a<b<=duration+40) for _,a,b in cues):
            raise ValueError("Invalid acoustic spans")
        if any(cues[i-1][2]>cues[i][1] for i in range(1,len(cues))):
            raise ValueError("Acoustic alignment overlapping words")
        return cues
