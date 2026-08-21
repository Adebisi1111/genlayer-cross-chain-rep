# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
from dataclasses import dataclass
from genlayer import *

# Cross-Chain Reputation Bridge


@allow_storage
@dataclass
class Snapshot:
    root: str
    timestamp: u256
    block_number: u256
    snapshotter: str


class ReputationBridge(gl.Contract):
    snapshots: TreeMap[u256, Snapshot]
    authorized_snapshotters: TreeMap[str, str]
    latest_snapshot_id: u256
    reputation_ledger: str

    def __init__(self):
        self.latest_snapshot_id = u256(0)
        self.reputation_ledger = ""

    @gl.public.write
    def setReputationLedger(self, ledger: str) -> None:
        if self.reputation_ledger != "":
            raise Exception("Reputation ledger already set.")
        self.reputation_ledger = ledger

    @gl.public.write
    def authorizeSnapshotter(self, snapshotter: str) -> None:
        self.authorized_snapshotters[snapshotter] = "1"

    @gl.public.write
    def submitSnapshot(self, merkle_root: str, block_number: u256) -> None:
        sender = gl.message.sender_address.as_hex
        if self.authorized_snapshotters.get(sender, "") != "1":
            raise Exception("Not an authorized snapshotter.")
        self.latest_snapshot_id += u256(1)
        self.snapshots[self.latest_snapshot_id] = Snapshot(
            root=merkle_root,
            timestamp=u256(0),
            block_number=block_number,
            snapshotter=sender,
        )

    @gl.public.view
    def getLatestSnapshot(self) -> str:
        snap = self.snapshots.get(self.latest_snapshot_id, None)
        if snap is None:
            return json.dumps({"exists": False})
        return json.dumps({
            "exists": True,
            "snapshot_id": int(self.latest_snapshot_id),
            "root": snap.root,
            "block_number": int(snap.block_number),
            "snapshotter": snap.snapshotter,
        })

    @gl.public.view
    def getSnapshot(self, snapshot_id: u256) -> str:
        snap = self.snapshots.get(snapshot_id, None)
        if snap is None:
            return json.dumps({"exists": False})
        return json.dumps({
            "exists": True,
            "snapshot_id": int(snapshot_id),
            "root": snap.root,
            "block_number": int(snap.block_number),
            "snapshotter": snap.snapshotter,
        })
