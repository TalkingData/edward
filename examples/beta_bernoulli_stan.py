#!/usr/bin/env python
"""
A simple coin flipping example. The model is written in Stan.
Inspired by Stan's toy example.

Probability model
    Prior: Beta
    Likelihood: Bernoulli
Variational model
    Likelihood: Mean-field Beta
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import edward as ed

from edward.models import Beta

model_code = """
    data {
      int<lower=0> N;
      int<lower=0,upper=1> y[N];
    }
    parameters {
      real<lower=0,upper=1> p;
    }
    model {
      p ~ beta(1.0, 1.0);
      for (n in 1:N)
        y[n] ~ bernoulli(p);
    }
"""
ed.set_seed(42)
model = ed.StanModel(model_code=model_code)
qp = Beta()
data = {'N': 10, 'y': [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]}

inference = ed.MFVI({'p': qp}, data, model)
inference.run(n_iter=10000)
