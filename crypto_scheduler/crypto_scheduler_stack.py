from aws_cdk import core

from crypto_scheduler.constructs.cb_pro_lambda import CbProLambda

class CryptoSchedulerStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cbProLambda = CbProLambda(self, "cb-pro-market-buy")
