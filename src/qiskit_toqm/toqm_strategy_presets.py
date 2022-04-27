# This code is part of Qiskit.
#
# (C) Copyright IBM 2022.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit_toqm import ToqmHeuristicStrategy, ToqmOptimalStrategy

# NOTE: currently, the heuristic mappers use the hard-coded latencies of 1, 2 and 6
# for 1Q, 2Q and SWAP gates, respectively. This is because when gate-specific latencies
# are used with heuristic components, the run sometimes never terminates.
# This is tracked here: https://github.com/qiskit-toqm/libtoqm/issues/15
from qiskit_toqm import latencies_from_simple


class ToqmStrategyO0:
    def __init__(self, latency_descriptions):
        self.heuristic_strategy = ToqmHeuristicStrategy(
            latency_descriptions,
            top_k=1,
            queue_target=3000,
            queue_max=5000
        )

    def __call__(self, coupling_map, gates, num_qubits):
        return self.heuristic_strategy(coupling_map, gates, num_qubits)


class ToqmStrategyO1:
    def __init__(self, latency_descriptions):
        # https://github.com/qiskit-toqm/libtoqm/issues/15
        latency_descriptions = latencies_from_simple(1, 2, 6)

        self.optimal_strategy = ToqmOptimalStrategy(
            latency_descriptions
        )

        self.heuristic_strategy = ToqmHeuristicStrategy(
            latency_descriptions,
            top_k=5,
            queue_target=400,
            queue_max=800
        )

    def __call__(self, coupling_map, gates, num_qubits):
        if coupling_map.numPhysicalQubits < 6:
            strategy = self.optimal_strategy
        else:
            strategy = self.heuristic_strategy

        return strategy(coupling_map, gates, num_qubits)


class ToqmStrategyO2:
    def __init__(self, latency_descriptions):
        # https://github.com/qiskit-toqm/libtoqm/issues/15
        latency_descriptions = latencies_from_simple(1, 2, 6)

        self.optimal_strategy = ToqmOptimalStrategy(
            latency_descriptions
        )

        self.heuristic_strategy = ToqmHeuristicStrategy(
            latency_descriptions,
            top_k=11,
            queue_target=400,
            queue_max=100
        )

    def __call__(self, coupling_map, gates, num_qubits):
        if coupling_map.numPhysicalQubits < 6:
            strategy = self.optimal_strategy
        else:
            strategy = self.heuristic_strategy

        return strategy(coupling_map, gates, num_qubits)


class ToqmStrategyO3:
    def __init__(self, latency_descriptions):
        # https://github.com/qiskit-toqm/libtoqm/issues/15
        latency_descriptions = latencies_from_simple(1, 2, 6)

        self.optimal_strategy = ToqmOptimalStrategy(
            latency_descriptions
        )

        self.optimal_strategy_no_swaps = ToqmOptimalStrategy(
            latency_descriptions,
            no_swaps=True
        )

        self.heuristic_strategy = ToqmHeuristicStrategy(
            latency_descriptions,
            top_k=3,
            queue_target=3600,
            queue_max=4800
        )

    def __call__(self, coupling_map, gates, num_qubits):
        if coupling_map.numPhysicalQubits < 6:
            # try no swaps first
            try:
                return self.optimal_strategy_no_swaps(coupling_map, gates, num_qubits)
            except RuntimeError:
                strategy = self.optimal_strategy
        else:
            strategy = self.heuristic_strategy

        return strategy(coupling_map, gates, num_qubits)
