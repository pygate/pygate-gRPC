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
    ],
    defaults=(None,) * 5,
)

CidSummary = namedtuple(
    "CidSummary", ["cid", "stored", "queuedJobs", "executingJob"], defaults=(None,) * 4,
)

StorageInfo = namedtuple("StorageInfo", ["job_id", "cid", "created", "hot", "cold"])

BuildInfo = namedtuple(
    "BuildInfo",
    ["gitCommit", "gitBranch", "gitState", "gitSummary", "buildDate", "version"],
)
