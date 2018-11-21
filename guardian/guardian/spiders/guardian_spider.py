import scrapy
from datetime import timedelta, datetime


class GuardianSpider(scrapy.Spider):
    """
        Spider to fetch values from guardian HTML
    """

    name = "guardian"
    start_urls = ["https://www.theguardian.com/au"]

    def __init__(self, num_of_days=2, *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)
        self.num_of_days = self.crawl_day_count = int(num_of_days)

    def parse(self, response):
        # Searching for primary categories/tabs in guardian online
        primary_tabs = response.xpath(
            '//ul[@class="menu-group menu-group--primary"]/li[@class="menu-item js-navigation-item"]')

        for index, tab in enumerate(primary_tabs):
            # The second tab contains opinions, rather than news, so it's skipped.
            if index != 1:
                category = tab.xpath('./@data-section-name').extract_first()

                # Iterating over sub-categories in each category
                for secondary_tab in tab.xpath('ul/li/a'):
                    sub_category = secondary_tab.xpath('./text()').extract_first()
                    sub_category_url = secondary_tab.xpath('./@href').extract_first()

                    date_to_process = datetime.today().date()

                    # Iterating reversely from today to the first day needed to recrawl
                    # controlled by num_of_days, which denotes how many days we need to consider
                    # Provided from terminal

                    while self.num_of_days:
                        formatted_date = date_to_process.strftime('%Y/%b/%d').lower()
                        news_url = "{}/{}/all".format(sub_category_url, formatted_date)

                        # HTTP request to load a subcategory page of a particular date
                        # response is passed to fetch_news_url callback
                        yield scrapy.Request(
                            response.urljoin(news_url),
                            callback=self.fetch_news_url,
                            meta={
                                'category': category,
                                'sub_category': sub_category,
                                'date': date_to_process
                            }
                        )

                        # Both the loop Counter and current date to process is re-evaluated
                        self.num_of_days -= 1
                        date_to_process = date_to_process - timedelta(days=1)

                    else:
                        # num_of_days is reset to inception value when loop is done
                        # So that the next sub-category gets proper value
                        self.num_of_days = self.crawl_day_count

    def fetch_news_url(self, response):
        pass