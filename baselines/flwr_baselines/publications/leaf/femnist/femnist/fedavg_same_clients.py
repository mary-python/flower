from typing import List, Tuple

from flwr.common import EvaluateIns, FitIns, Parameters
from flwr.server import ClientManager
from flwr.server.client_proxy import ClientProxy
from flwr.server.strategy import FedAvg


class FedAvgSameClients(FedAvg):
    """FedAvg that samples clients for each round only once (the same clinets
    are used for training and testing round n)

    It does not mean that the same client are used in each round. It used just the same clients (with different parts of their data) in round i.

    It assumes that there is no different function for evaluation - on_evaluate_config_fn (it's ignored).
    """

    def configure_fit(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, FitIns]]:
        """Configure the next round of training."""
        self._current_round_fit_clients_fits_list = super().configure_fit(
            server_round, parameters, client_manager
        )
        # Return client/config pairs
        return self._current_round_fit_clients_fits_list

    def configure_evaluate(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, EvaluateIns]]:
        # Keep the fraction_settings for consistency reasons
        if self.fraction_evaluate == 0.0:
            return []
        evaluate_config = []
        for tuple_client_proxy_fit_ins in self._current_round_fit_clients_fits_list:
            eval_ins = EvaluateIns(
                tuple_client_proxy_fit_ins[1].parameters,
                tuple_client_proxy_fit_ins[1].config,
            )
            evaluate_config.append((tuple_client_proxy_fit_ins[0], eval_ins))
        return evaluate_config