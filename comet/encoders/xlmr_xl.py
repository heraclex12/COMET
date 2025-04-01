# -*- coding: utf-8 -*-
# Copyright (C) 2020 Unbabel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""
XLM-RoBERTa-XL Encoder
==============
    Pretrained XLM-RoBERTa-XL  encoder from Hugging Face.
"""
from transformers import XLMRobertaTokenizerFast, XLMRobertaXLConfig, XLMRobertaXLModel
import torch
from comet.encoders.base import Encoder
from comet.encoders.xlmr import XLMREncoder


class XLMRXLEncoder(XLMREncoder):
    """XLM-RoBERTA-XL Encoder encoder.

    Args:
        pretrained_model (str): Pretrained model from hugging face.
        load_pretrained_weights (bool): If set to True loads the pretrained weights
            from Hugging Face
        local_files_only (bool): Whether or not to only look at local files.
    """

    def __init__(
        self,
        pretrained_model: str,
        load_pretrained_weights: bool = True,
        local_files_only: bool = False,
    ) -> None:
        super(Encoder, self).__init__()
        self.tokenizer = XLMRobertaTokenizerFast.from_pretrained(
            pretrained_model, local_files_only=local_files_only
        )
        if load_pretrained_weights:
            self.model = XLMRobertaXLModel.from_pretrained(
                pretrained_model, add_pooling_layer=False, torch_dtype=torch.float16, device_map="auto"
            )
        else:
            self.model = XLMRobertaXLModel(
                XLMRobertaXLConfig.from_pretrained(
                    pretrained_model, local_files_only=local_files_only, torch_dtype=torch.float16, device_map="auto"
                ),
                add_pooling_layer=False,
            )
        self.model.encoder.output_hidden_states = True

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model: str,
        load_pretrained_weights: bool = True,
        local_files_only: bool = False,
    ) -> Encoder:
        """Function that loads a pretrained encoder from Hugging Face.

        Args:
            pretrained_model (str): Name of the pretrain model to be loaded.
            load_pretrained_weights (bool): If set to True loads the pretrained weights
                from Hugging Face
            local_files_only (bool): Whether or not to only look at local files.

        Returns:
            Encoder: XLMRXLEncoder object.
        """
        return XLMRXLEncoder(
            pretrained_model, load_pretrained_weights, local_files_only
        )
