from aws_cdk import (
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    core,
)

import os
import subprocess

class CbProLambda(core.Construct):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cb_pro_lambda = _lambda.Function(
            self, 
            id='CbProMarketBuy',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('crypto_scheduler/lambdas/cb_pro'),
            handler='market_buy.lambda_handler',
            layers=[self.create_dependencies_layer("CbProMarketBuy")]
        )

        self.create_schedule(cb_pro_lambda)

    ''' Set schedule for lambda '''
    # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_events/Schedule.html
    def create_schedule(self, cb_pro_lambda):
        lambdaTarget = targets.LambdaFunction(handler=cb_pro_lambda)
        lambdaEventRule = events.Rule(
            scope=self,
            id="market-buy-schedule",
            rule_name="market-buy-schedule",
            targets=[lambdaTarget],
            description="Scheduled market orders on CB pro",
            schedule=events.Schedule.expression("rate(1 day)") # https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html
        )

    ''' Packages third party dependencies '''
    def create_dependencies_layer(self, function_name: str) -> _lambda.LayerVersion:
        requirements_file = "crypto_scheduler/lambdas/resources/dependencies.txt"
        output_dir = ".lambda_dependencies/" + function_name
        
        # Install requirements for layer in the output_dir
        if not os.environ.get("SKIP_PIP"):
            # Note: Pip will create the output dir if it does not exist
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}/python".split()
            )
        return _lambda.LayerVersion(
            self,
            function_name + "-dependencies",
            code=_lambda.Code.from_asset(output_dir)
        )