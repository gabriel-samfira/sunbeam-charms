import re
from typing import List
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def parse_cert_chain(pem_data: str) -> List[x509.Certificate]:
    ca_chain = re.findall(
        r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
        pem_data,
        re.DOTALL
    )

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
        parsed_chain = parse_cert_chain(chain)
    except ValueError:
        return False
    if not parsed_chain:
        return False
    return True
