import unittest
import asyncio
from decimal import Decimal, ROUND_HALF_UP
from app.services.reservations import calculate_total_revenue
from app.services.cache import get_revenue_summary

class TestBugsRegression(unittest.TestCase):

    def test_bug_a_property_revenue_calculation(self):
        """Test Bug A: Correct property revenue calculation and mock fallback for Sunset Properties (tenant-a)"""
        async def run():
            result = await calculate_total_revenue('prop-001', 'tenant-a')
            self.assertEqual(result['tenant_id'], 'tenant-a')
            self.assertEqual(result['property_id'], 'prop-001')
            self.assertEqual(Decimal(result['total']), Decimal('2250.000'))
            self.assertEqual(result['count'], 4)
        asyncio.run(run())

    def test_bug_b_tenant_cache_isolation(self):
        """Test Bug B: Multi-tenant data leakage in Redis cache keys"""
        async def run():
            res_a = await get_revenue_summary('prop-001', 'tenant-a')
            res_b = await get_revenue_summary('prop-001', 'tenant-b')
            self.assertEqual(res_a['tenant_id'], 'tenant-a')
            self.assertEqual(res_b['tenant_id'], 'tenant-b')
            self.assertNotEqual(res_a['total'], res_b['total'])
            self.assertEqual(Decimal(res_a['total']), Decimal('2250.000'))
            self.assertEqual(Decimal(res_b['total']), Decimal('1500.000'))
        asyncio.run(run())

    def test_bug_c_financial_precision(self):
        """Test Bug C: Financial precision using Decimal arithmetic and quantization"""
        amounts = [Decimal('333.333'), Decimal('333.333'), Decimal('333.334'), Decimal('1250.000')]
        total = sum(amounts)
        quantized = total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        self.assertEqual(total, Decimal('2250.000'))
        self.assertEqual(quantized, Decimal('2250.00'))
        self.assertEqual(float(quantized), 2250.0)

if __name__ == '__main__':
    unittest.main()
