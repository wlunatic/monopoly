import os
from datetime import datetime

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from monopoly.banks.ocbc.credit import Ocbc365
from monopoly.constants import AMOUNT, DATE, DESCRIPTION, ROOT_DIR


@pytest.mark.parametrize("statement_date", [datetime(2024, 1, 1)])
def test_ocbc_write_to_local_csv(date_specific_ocbc: Ocbc365):
    transformed_df = pd.DataFrame(
        [
            {
                DATE: "2024-01-12",
                DESCRIPTION: "FAIRPRICE FINEST SINGAPORE SG",
                AMOUNT: 18.49,
            },
            {
                DATE: "2023-12-28",
                DESCRIPTION: "DA PAOLO GASTRONOMIA SING — SINGAPORE SG",
                AMOUNT: 19.69,
            },
        ]
    )

    date_specific_ocbc.load(transformed_df)

    local_df = pd.read_csv(os.path.join(ROOT_DIR, "output", "OCBC-365-2024-01.csv"))
    assert_frame_equal(transformed_df, local_df)
