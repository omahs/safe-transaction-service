from django.core.management import BaseCommand

import requests

from gnosis.eth import EthereumClientProvider

from safe_transaction_service.contracts.models import Contract


class Command(BaseCommand):
    help = "Update safe contract logos by new one"
    safe_deployments_base_url = (
        "https://raw.githubusercontent.com/safe-global/safe-deployments/main/src/assets"
    )
    deployment_paths = {
        "v1.3.0": [
            "compatibility_fallback_handler.json",
            "create_call.json",
            "gnosis_safe.json",
            "gnosis_safe_l2.json",
            "multi_send.json",
            "multi_send_call_only.json",
            "proxy_factory.json",
            "sign_message_lib.json",
            "simulate_tx_accessor.json",
        ]
    }

    def add_arguments(self, parser):
        parser.add_argument(
            "--safe-version", type=str, help="Contract version", required=True
        )
        parser.add_argument(
            "--logo-path", type=str, help="Path of new logo", required=True
        )

    def handle(self, *args, **options):
        safe_version = options["safe_version"]
        logo_path = options["logo_path"]
        # TODO create ProcessedImageField from path
        # TODO add 1.1.1
        accepted_versions = ["1.3.0"]
        if safe_version not in accepted_versions:
            self.stdout.write(
                self.style.ERROR(f"safe version should be one of {accepted_versions} ")
            )
            return None

        ethereum_client = EthereumClientProvider()
        chain_id = ethereum_client.get_chain_id()

        for deployment_path in self.deployment_paths[safe_version]:
            result = requests.get(
                f"{self.safe_deployments_base_url}/{safe_version}/{deployment_path}"
            )
            deployment = result.json()
            address = deployment[str(chain_id)]
            try:
                contract = Contract.objects.get(address=address)
                # TODO update logo to the new one
                # TODO ensure display is Safe
            except Contract.DoesNotExist:
                # Ignore contracts that those not exist
                pass
