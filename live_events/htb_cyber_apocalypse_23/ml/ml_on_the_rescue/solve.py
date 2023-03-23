import torch
import torch.nn as nn
from torch.nn import functional as F
torch.manual_seed(1337)

vocab = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}\n")

class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):

        logits = self.token_embedding_table(idx) 
        
        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits
    
model = BigramLanguageModel(93)
model.load_state_dict(torch.load('./bigram_model.pt'))
model.eval()

def test_input(flag: str):
    # Tokenize the input string into individual characters
    tokens = list(flag)

    # Convert the tokens to their corresponding integer indices using the vocab list
    indices = [vocab.index(token) for token in tokens]

    # Create a tensor of the indices
    input_tensor = torch.tensor(indices)
    output_logits = model(input_tensor)
    return output_logits

flag = "H"
for i in range(93):
    test = flag + ("A"*(93-len(flag)))
    out = test_input(test)
    argmax = list(torch.argmax(out, dim=1))
    index = int(argmax[i])
    flag += vocab[index]

print(flag)
