import pytest
from ignovex.models import HolderRecord, TokenDistribution


def make_dist(
    holders=None,
    total_supply=1_000_000.0,
    lp_balance=0.0,
    token_mint="So111111111111111111111111111111111111112",
):
    if holders is None:
        holders = []
    return TokenDistribution(
        token_mint=token_mint,
        total_supply=total_supply,
        holders=holders,
        lp_total_balance=lp_balance,
    )


@pytest.fixture
def equal_dist():
    """10 holders each with 100k tokens, all old wallets — perfectly equal."""
    holders = [
        HolderRecord(address=f"wallet{i}", balance=100_000.0, wallet_age_days=30.0)
        for i in range(10)
    ]
    return make_dist(holders=holders, total_supply=1_000_000.0)


@pytest.fixture
def concentrated_dist():
    """1 whale with 900k, 9 small holders with ~11k each."""
    holders = [HolderRecord(address="whale", balance=900_000.0, wallet_age_days=60.0)]
    holders += [
        HolderRecord(address=f"small{i}", balance=11_111.0, wallet_age_days=30.0)
        for i in range(9)
    ]
    return make_dist(holders=holders, total_supply=1_000_000.0)


@pytest.fixture
def fresh_wallet_dist():
    """5 old holders, 5 fresh holders (<7 days)."""
    holders = [
        HolderRecord(address=f"old{i}", balance=100_000.0, wallet_age_days=30.0)
        for i in range(5)
    ]
    holders += [
        HolderRecord(address=f"new{i}", balance=100_000.0, wallet_age_days=2.0)
        for i in range(5)
    ]
    return make_dist(holders=holders, total_supply=1_000_000.0)


@pytest.fixture
def lp_heavy_dist():
    """LP holds 600k of 1M supply."""
    holders = [
        HolderRecord(address=f"h{i}", balance=50_000.0, wallet_age_days=30.0)
        for i in range(8)
    ]
    return make_dist(holders=holders, total_supply=1_000_000.0, lp_balance=600_000.0)


@pytest.fixture
def dominated_dist():
    """Max risk: 1 whale with 950k, 50% fresh wallets, LP holds 600k."""
    holders = [HolderRecord(address="bigwhale", balance=950_000.0, wallet_age_days=90.0)]
    holders += [
        HolderRecord(address=f"new{i}", balance=1_000.0, wallet_age_days=1.0)
        for i in range(25)
    ]
    holders += [
        HolderRecord(address=f"old{i}", balance=1_000.0, wallet_age_days=30.0)
        for i in range(25)
    ]
    return make_dist(holders=holders, total_supply=2_000_000.0, lp_balance=600_000.0)
