import logging
from re import compile as regex

from monopoly.config import StatementConfig
from monopoly.constants import (
    BankNames,
    DebitTransactionPatterns,
    EntryType,
)
from monopoly.identifiers import MetadataIdentifier, TextIdentifier

from ..base import BankBase

logger = logging.getLogger(__name__)


class Gxs(BankBase):
    debit_config = StatementConfig(
        statement_type=EntryType.DEBIT,
        bank_name=BankNames.GXS,
        statement_date_pattern=regex(r"(\d{2}\s[A-Za-z]{3}\s\d{4})"),
        multiline_transactions=True,
        header_pattern=regex(r"(Withdrawal.*Deposit.*Balance)"),
        transaction_pattern=DebitTransactionPatterns.GXS,
    )

    identifiers = [
        [
            TextIdentifier("GXS"),
            MetadataIdentifier(creator="Chromium", producer="Skia/PDF m117"),
        ],
    ]

    statement_configs = [debit_config]
