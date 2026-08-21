import json


def _hex(addr):
    if isinstance(addr, bytes):
        return "0x" + addr.hex()
    return str(addr)


def test_set_ledger_and_authorize(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/reputation_bridge.py")
    direct_vm.sender = direct_alice
    contract.setReputationLedger(_hex(direct_alice))
    contract.authorizeSnapshotter(_hex(direct_alice))
    print("LEDGER SET + AUTHORIZED")


def test_submit_snapshot(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/reputation_bridge.py")
    direct_vm.sender = direct_alice
    contract.setReputationLedger(_hex(direct_alice))
    contract.authorizeSnapshotter(_hex(direct_alice))
    contract.submitSnapshot("0xabc123", 1000)
    snap = json.loads(contract.getLatestSnapshot())
    assert snap["exists"] is True
    assert snap["root"] == "0xabc123"
    print("SNAPSHOT SUBMITTED")


def test_unauthorized_snapshot_reverts(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/reputation_bridge.py")
    direct_vm.sender = direct_alice
    contract.setReputationLedger(_hex(direct_alice))
    contract.authorizeSnapshotter(_hex(direct_alice))
    direct_vm.sender = direct_bob
    try:
        contract.submitSnapshot("0xdef456", 2000)
        raise AssertionError("expected revert: bob not authorized")
    except Exception as e:
        assert "Not an authorized" in str(e)
    print("UNAUTHORIZED REVERT OK")


def test_get_snapshot(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/reputation_bridge.py")
    direct_vm.sender = direct_alice
    contract.setReputationLedger(_hex(direct_alice))
    contract.authorizeSnapshotter(_hex(direct_alice))
    contract.submitSnapshot("0xabc123", 1000)
    snap = json.loads(contract.getSnapshot(1))
    assert snap["exists"] is True
    assert snap["root"] == "0xabc123"
    assert snap["block_number"] == 1000
    print("GET SNAPSHOT OK")
