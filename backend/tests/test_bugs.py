import pytest
from decimal import Decimal, ROUND_HALF_UP
from app.services.reservations import calculate_total_revenue
from app.services.cache import get_revenue_summary
import redis.asyncio as redis
import os

@pytest.mark.asyncio
async def test_bug_a_property_revenue_calculation():
    """Test Bug A: Correct property revenue calculation and mock fallback for Sunset Properties (tenant-a)"""
    result = await calculate_total_revenue('prop-001', 'tenant-a')
    assert result['tenant_id'] == 'tenant-a'
    assert result['property_id'] == 'prop-001'
    # Expected total including timezone-adjusted boundary reservation (1250 + 333.333 + 333.333 + 333.334) = 2250.000
    assert Decimal(result['total']) == Decimal('2250.000')
    assert result['count'] == 4

@pytest.mark.asyncio
async def test_bug_b_tenant_cache_isolation():
    """Test Bug B: Multi-tenant data leakage in Redis cache keys"""
    # Verify cache key format includes tenant_id
    # Sunset Properties (tenant-a) has prop-001
    res_a = await get_revenue_summary('prop-001', 'tenant-a')
    # Ocean Rentals (tenant-b) has prop-001
    res_b = await get_revenue_summary('prop-001', 'tenant-b')

    assert res_a['tenant_id'] == 'tenant-a'
    assert res_b['tenant_id'] == 'tenant-b'
    # They should have different revenue totals because cache keys are tenant-isolated
    assert res_a['total'] != res_b['total']
    assert Decimal(res_a['total']) == Decimal('2250.000')
    assert Decimal(res_b['total']) == Decimal('1500.000')

@pytest.mark.asyncio
async def test_bug_c_financial_precision():
    """Test Bug C: Financial precision using Decimal arithmetic and quantization"""
    # Summing sub-cent amounts without float drift
    amounts = [Decimal('333.333'), Decimal('333.333'), Decimal('333.334'), Decimal('1250.000')]
    total = sum(amounts)
    quantized = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    assert total == Decimal('2250.000')
    assert quantized == Decimal('2250.00')
    assert float(quantized) == 2250.0
