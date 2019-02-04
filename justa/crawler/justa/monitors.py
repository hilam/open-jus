from spidermon import Monitor, MonitorSuite, monitors


class MinimumItemsMonitor(Monitor):
    minimum_expected = {
        'DF': 433,
        'SP': 826
    }

    @monitors.name('Minimum number of items')
    def test_minimum_number_of_items(self):
        spider = self.data['spider']
        items_extracted = self.data.stats.get('item_scraped_count', 0)
        minimum_expected = self.minimum_expected.get(spider.abbr, 0)
        self.assertGreaterEqual(items_extracted, minimum_expected)


class JustaMonitorSuite(MonitorSuite):
    monitors = [MinimumItemsMonitor]
