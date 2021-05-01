#!/usr/bin/env python3

from aws_cdk import core

from crypto_scheduler.crypto_scheduler_stack import CryptoSchedulerStack


app = core.App()
CryptoSchedulerStack(app, "crypto-scheduler")

app.synth()
