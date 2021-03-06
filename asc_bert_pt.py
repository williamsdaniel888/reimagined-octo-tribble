from transformers.modeling_albert import AlbertPreTrainedModel, AlbertModel
import torch
from torch.autograd import Variable, grad

class AlbertForABSA(AlbertModel):
    def __init__(self, config, num_labels=3, dropout=None):
        super(AlbertForABSA, self).__init__(config)
        self.num_labels = num_labels
        self.albert = AlbertModel(config)
        self.dropout = torch.nn.Dropout(dropout)
        self.classifier = torch.nn.Linear(config.hidden_size, num_labels)
        self.init_weights

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None):
        _, pooled_output = self.albert(input_ids, token_type_ids, attention_mask)#, output_all_encoded_layers=False)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        if labels is not None:
            loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-1)
            _loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            return _loss
        else:
            return logits

