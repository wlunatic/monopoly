import logging
from re import compile as regex

from monopoly.config import StatementConfig
from monopoly.constants import (
    BankNames,
    DebitTransactionPatterns,
    EntryType,
)
from monopoly.constants.date import ISO8601
from monopoly.identifiers import MetadataIdentifier, TextIdentifier

from ..base import BankBase

logger = logging.getLogger(__name__)


class Gxs(BankBase):
    name = BankNames.GXS
    
    debit = StatementConfig(
        statement_type=EntryType.DEBIT,
        statement_date_pattern=ISO8601.DD_MMM_YYYY,
        multiline_transactions=True,
        header_pattern=regex(r"(Withdrawal.*Deposit.*Balance)"),
        transaction_pattern=DebitTransactionPatterns.GXS,
        safety_check=False
    )

    identifiers = [
        [
            TextIdentifier("GXS"),
            MetadataIdentifier(creator="Chromium", producer="Skia/PDF m117"),
        ],
    ]

    statement_configs = [debit]
