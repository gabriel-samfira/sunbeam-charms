import re
import utils
from typing import List
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def parse_cert_chain(ca_chain: List[str]) -> List[x509.Certificate]:
    parsed_certs = []
    for idx, pem_cert in enumerate(ca_chain):
        try:
            cert = x509.load_pem_x509_certificate(
                pem_cert.encode(), default_backend()
            )
            parsed_certs.append(cert)
        except Exception as e:
            raise ValueError(
                f"Certificate #{idx+1} is corrupted or invalid: {e}"
            )

    return parsed_certs


def is_valid_chain(chain: str) -> bool:
    try:
        cert_list = utils.parse_ca_chain(chain)
        if not cert_list:
            return False
        parsed_chain = parse_cert_chain(cert_list)
    except ValueError:
        return False
    if not parsed_chain:
        return False
    return True
