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
Feed Forward
============
    Feed Forward Neural Network module that can be used for classification or regression
"""
from typing import List, Optional

import torch
from torch import nn


class FeedForward(nn.Module):
    """Feed Forward Neural Network.

    Args:
        in_dim (int): Number input features.
        out_dim (int): Number of output features. Default is just a score.
        hidden_sizes (List[int]): List with hidden layer sizes. Defaults to [3072,1024]
        activations (str): Name of the activation function to be used in the hidden
            layers. Defaults to 'Tanh'.
        final_activation (Optional[str]): Final activation if any.
        dropout (float): dropout to be used in the hidden layers.
    """

    def __init__(
        self,
        in_dim: int,
        out_dim: int = 1,
        hidden_sizes: List[int] = [3072, 1024],
        activations: str = "Tanh",
        final_activation: Optional[str] = None,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()
        modules = []
        modules.append(nn.Linear(in_dim, hidden_sizes[0]))
        modules.append(self.build_activation(activations))
        modules.append(nn.Dropout(dropout))

        for i in range(1, len(hidden_sizes)):
            modules.append(nn.Linear(hidden_sizes[i - 1], hidden_sizes[i]))
            modules.append(self.build_activation(activations))
            modules.append(nn.Dropout(dropout))

        modules.append(nn.Linear(hidden_sizes[-1], int(out_dim)))
        if final_activation is not None:
            modules.append(self.build_activation(final_activation))

        self.ff = nn.Sequential(*modules)

    def build_activation(self, activation: str) -> nn.Module:
        if hasattr(nn, activation.title()):
            return getattr(nn, activation.title())()
        else:
            raise Exception(f"{activation} is not a valid activation function!")

    def forward(self, in_features: torch.Tensor) -> torch.Tensor:
        # When casting models to float 16 self.ff(in_features) was giving some problems reported
        # in here: https://huggingface.co/Unbabel/wmt23-cometkiwi-da-xl/discussions/3

        # Check the dtype of self.ff parameters
        ff_dtypes = {param.dtype for param in self.ff.parameters()}
        
        # If all parameters are float16 and in_features is not, convert it
        if ff_dtypes == {torch.float16} and in_features.dtype != torch.float16:
            in_features = in_features.to(torch.float16)
        
        return self.ff(in_features)
