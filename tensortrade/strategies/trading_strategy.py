# Copyright 2019 The TensorTrade Authors.
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

import pandas as pd
import numpy as np

from abc import ABCMeta, abstractmethod
from typing import Union, Callable, List

from tensortrade.environments.trading_environment import TradingEnvironment
from tensortrade.features.feature_pipeline import FeaturePipeline


class TradingStrategy(object, metaclass=ABCMeta):
    """An abstract trading strategy capable of self tuning, training, and evaluating."""

    @abstractmethod
    def __init__(self, environment: TradingEnvironment):
        """
        Arguments:
            environment: A `TradingEnvironment` instance for the agent to trade within.
        """
        self._environment = environment

    @property
    def environment(self) -> TradingEnvironment:
        """A `TradingEnvironment` instance for the agent to trade within."""
        return self._environment

    @environment.setter
    def environment(self, environment: TradingEnvironment):
        self._environment = environment

    @abstractmethod
    def restore_agent(self, path: str):
        """Deserialize the strategy's learning agent from a file.

        Arguments:
            path: The `str` path of where the strategy is stored.
        """
        raise NotImplementedError

    @abstractmethod
    def save_agent(self, path: str):
        """Serialize the strategy's learning agent to a file for restoring later.

        Arguments:
            path: The `str` path of where to store the strategy.
        """
        raise NotImplementedError

    @abstractmethod
    def tune(self, steps_per_train: int, steps_per_test: int, step_cb: Callable[[pd.DataFrame], bool] = None) -> pd.DataFrame:
        """Tune the agent's hyper-parameters and feature set for the environment.

        Arguments:
            steps_per_train: The number of steps per training of each hyper-parameter set.
            steps_per_test: The number of steps per evaluation of each hyper-parameter set.
            step_cb (optional): A callback function for monitoring progress of the tuning process.
                step_cb(pd.DataFrame) -> bool: A history of the agent's trading performance is passed on each iteration.
                If the callback returns `True`, the training process will stop early.

        Returns:
            A history of the agent's trading performance during tuning
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, steps: int = None, episodes: int = None, should_train: bool = False, callback: Callable[[pd.DataFrame], bool] = None) -> pd.DataFrame:
        """Evaluate the agent's performance within the environment.

        Arguments:
            steps: The number of steps to run the agent within the environment. Required if `episodes` is not passed.
            episodes: The number of episodes to run the agent within the environment. Required if `steps` is not passed.
            should_train: Whether or not the agent should be trained on the environment it is running in. Defaults to false.
            step_cb (optional): A callback function for monitoring the agent's progress within the environment.
                step_cb(pd.DataFrame) -> bool: A history of the agent's trading performance is passed on each iteration.
                If the callback returns `True`, the training process will stop early.

        Returns:
            A history of the agent's trading performance during evaluation
        """
        raise NotImplementedError
