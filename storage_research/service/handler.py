import logging

import matplotlib.pyplot as plt
import pandas as pd

from storage_research.settings.config import (RESULT_DIR, mongo_config,
                                              pg_config)

log = logging.getLogger(__name__)


def handler_result():
    df1 = pd.read_csv(
        mongo_config.mongo_result_r,
        header=None,
        names=["operation", "func", "time", "count"],
    )
    df2 = pd.read_csv(
        pg_config.pg_result_r, header=None, names=["operation", "func", "time", "count"]
    )
    plt.plot(df1["count"], df1["time"].rolling(10).mean(), label="mongo")
    plt.plot(df2["count"], df2["time"].rolling(10).mean(), label="pg")
    plt.legend()
    plt.savefig(RESULT_DIR.joinpath("read.png"))
    plt.close()
    df1 = pd.read_csv(
        mongo_config.mongo_result_w,
        header=None,
        names=["operation", "func", "time", "count"],
    )
    df2 = pd.read_csv(
        pg_config.pg_result_w, header=None, names=["operation", "func", "time", "count"]
    )
    plt.plot(df1["count"], df1["time"].rolling(10).mean(), label="mongo")
    plt.plot(df2["count"], df2["time"].rolling(10).mean(), label="pg")
    plt.legend()
    plt.savefig(RESULT_DIR.joinpath("wright.png"))
    plt.close()


if __name__ == "__main__":
    handler_result()
