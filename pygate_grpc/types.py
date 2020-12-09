from collections import namedtuple

User = namedtuple("User", ["id", "token"])
StagedFile = namedtuple("StagedFile", ["cid"])
Address = namedtuple("Address", ["name", "address", "type", "balance"])
Job = namedtuple("Job", ["jobId"])
CidInfo = namedtuple(
    "CidInfo",
    [
        "cid",
        "latestPushedStorageConfig",
        "executingStorageJob",
        "queuedStorageJobs",
        "currentStorageInfo",
        "latestFinalStorageJob",
        "latestSuccessfulStorageJob",
    ],
    defaults=(None,) * 7,
)
BuildInfo = namedtuple(
    "BuildInfo",
    ["gitCommit", "gitBranch", "gitState", "gitSummary", "buildDate", "version"],
)
