import logging
from functools import cached_property

from monopoly.banks import BankBase
from monopoly.config import StatementConfig
from monopoly.constants import EntryType, InternalBankNames
from monopoly.handler import StatementHandler
from monopoly.pdf import PdfParser

from .generic import DatePatternAnalyzer

logger = logging.getLogger(__name__)


class GenericBank(BankBase):
    """
    Empty bank class with variables that can be populated by
    the `GenericStatementHandler` class
    """

    # populated by generic statement handler
    @property
    def statement_configs(self):
        return None

    @property
    def identifiers(self):
        return None


class GenericStatementHandler(StatementHandler):
    def __init__(self, parser: PdfParser):
        pages = parser.get_pages()
        self.analyzer = DatePatternAnalyzer(pages)
        parser.bank.statement_configs = list(
            filter(None, [self.debit_config, self.credit_config])
        )
        super().__init__(parser)

    # override get_header and ignore passed config, since
    # the header line has already been found
    def get_header(self, _: StatementConfig):
        return self.header_pattern

    @cached_property
    def debit_config(self):
        if self.statement_type == EntryType.DEBIT:
            logger.debug("Creating debit statement config")

            return StatementConfig(
                statement_type=EntryType.DEBIT,
                bank_name=InternalBankNames.GENERIC,
                transaction_pattern=self.transaction_pattern,
                statement_date_pattern=self.statement_date_pattern,
                multiline_transactions=self.multiline_transactions,
                header_pattern=self.header_pattern,
            )
        return None

    @cached_property
    def credit_config(self):
        if self.statement_type == EntryType.CREDIT:
            logger.debug("Creating credit statement config")

            return StatementConfig(
                statement_type=EntryType.CREDIT,
                bank_name=InternalBankNames.GENERIC,
                prev_balance_pattern=self.prev_balance_pattern,
                transaction_pattern=self.transaction_pattern,
                statement_date_pattern=self.statement_date_pattern,
                header_pattern=self.header_pattern,
                multiline_transactions=self.multiline_transactions,
            )
        return None

    @cached_property
    def transaction_pattern(self):
        return self.analyzer.create_transaction_pattern()

    @cached_property
    def statement_type(self):
        return self.analyzer.get_statement_type()

    @cached_property
    def statement_date_pattern(self):
        return self.analyzer.create_statement_date_pattern()

    @cached_property
    def multiline_transactions(self):
        return self.analyzer.check_if_multiline()

    @cached_property
    def header_pattern(self):
        lines = self.analyzer.lines_before_first_transaction
        return self.analyzer.get_debit_statement_header_line(lines)

    @cached_property
    def prev_balance_pattern(self):
        return self.analyzer.create_previous_balance_regex()
