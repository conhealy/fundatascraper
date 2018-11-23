"""
Module containing class for scraping a single mutual fund profile on
fundata.com
"""
import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd


class FundProfileScraper:
    """
    Class for scraping details from a specific mutual fund page on fundata.com
    """
    def __init__(self, url):
        self.soup = BeautifulSoup(urllib2.urlopen(url), 'html.parser')

    def scrape_all_single_value(self):
        """
        Scrapes all values from the fund page that represent a single valued
        metric i.e. not part of a list or table of values.
        """
        top_fund_nums = self.scrape_nums_top()
        info_table = self.scrape_info_table()
        info_panel = self.scrape_info_panel()
        return_table = self.scrape_return_table()
        calendar_returns = self.scrape_calendar_return()

        concatenated_dict = {**top_fund_nums, **info_table, **info_panel,
                             **return_table, **calendar_returns}

        return concatenated_dict


    def scrape_nums_top(self):
        """
        Extract values for inception return, ytd_return, navps, and change
        located underneath the title heading at the top of the page.
        """
        inception_return = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtInceptionReturn"})
            .text
        )

        ytd_return = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtYTDReturn"}).text
        )

        navps = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtNavps"})
            .text
        )

        change = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtNavpsChange"})
            .text
        )

        return {"inception_return": inception_return,
                "ytd_return": ytd_return,
                "navps": navps,
                "change": change}


    def scrape_info_table(self):
        """
        Extract vales in the table to the right of the growth chart on the
        page.
        """
        mer = self.soup.find("span", {"id": "ctl00_MainContent_txtMER"}).text

        assets = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtAssets"}).text
        )

        rank = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtRank"}).text
        )

        std_dev = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtStdDev"}).text
        )

        vol_rank = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtVolatilityRank"})
            .text
        )

        load = self.soup.find("span", {"id": "ctl00_MainContent_txtLoad"}).text

        max_front_end = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtFeesFront"})
            .text
        )

        max_back_end = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtFeesBack"})
            .text
        )

        sales_status = (
            self.soup
            .find("span", {"id": "ctl00_MainContent_txtSalesStatus"})
            .text
        )

        return {"mer": mer,
                "assets": assets,
                "rank": rank,
                "std_dev": std_dev,
                "volatility_rank": vol_rank,
                "load": load,
                "max_front_end": max_front_end,
                "max_back_end": max_back_end,
                "sales_status": sales_status}


    def scrape_info_panel(self):
        """
        Extract info on objective, manageent co, and fund managers from the
        panel immediately below the growth chart.
        """
        objective = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtObjective"}).text
        )

        management_co = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtManagementCo"}).text
        )

        fund_managers = (
            self.soup.find("span", {"id": "ctl00_MainContent_txtManagers"}).text
        )

        return {"objective_description": objective,
                "management_co": management_co,
                "fund_managers": fund_managers}


    def scrape_asset_allocation(self):
        """Extract asset allocation info."""
        asset_map = (
            self.soup
            .find("map", {"id": "ctl00$MainContent$chrtAssetAllocationImageMap"})
            .findAll("area")
        )

        return [x["title"] for x in asset_map]


    def scrape_sector_allocation(self):
        """Extract sector allocation info."""
        sector_map = (
            self.soup
            .find("map", {"id": "ctl00$MainContent$chrtSectorAllocationImageMap"})
            .findAll("area")
        )

        return [x["title"] for x in sector_map]


    def scrape_geo_allocation(self):
        """Extract geo allocation info."""
        geo_map = (
            self.soup
            .find("map", {"id": "ctl00$MainContent$chrtGeoAllocationImageMap"})
            .findAll("area")
        )

        return [x["title"] for x in geo_map]


    def scrape_top10_holdings(self):
        """Extract details of top 10 holdings."""
        table_rows = (
            self.soup
            .find("table", {"id": "ctl00_MainContent_gvTopTenHoldings"})
            .findAll("tr")
        )

        holding_list = []
        for html_tr in table_rows:
            html_td = html_tr.find_all('td')
            row = [tr.text for tr in html_td]
            holding_list.append(row)

        return pd.DataFrame(holding_list)

    def scrape_return_table(self):
        #pylint: disable-msg=too-many-locals
        """
        Extract returns data from performance section at bottom of page.
        """
        # Fund
        fs1mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtFS1mthRtn"})
                     .text)
        fs3mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtFS3mthRtn"})
                     .text)
        fs6mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtFS6mthRtn"})
                     .text)
        fsytdrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtFSytdRtn"})
                    .text)
        fc1yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtFC1yrRtn"})
                    .text)
        fc3yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtFC3yrRtn"})
                    .text)
        fc5yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtFC5yrRtn"})
                    .text)
        fc10yrrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtFC10yrRtn"})
                     .text)

        # Benchmark
        is1mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtIS1mthRtn"})
                     .text)
        is3mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtIS3mthRtn"})
                     .text)
        is6mthrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtIS6mthRtn"})
                     .text)
        isytdrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtISytdRtn"})
                    .text)
        ic1yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtIC1yrRtn"})
                    .text)
        ic3yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtIC3yrRtn"})
                    .text)
        ic5yrrtn = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtIC5yrRtn"})
                    .text)
        ic10yrrtn = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtIC10yrRtn"})
                     .text)

        # Quartiile ranking
        s1mthqrank = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtS1mthqrank"})
                      .text)
        s3mthqrank = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtS3mthqrank"})
                      .text)
        s6mthqrank = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtS6mthqrank"})
                      .text)
        sytdrank = (self.soup
                    .find("span", {"id": "ctl00_MainContent_txtSytdrank"})
                    .text)
        c1yrqrank = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtC1yrqrank"})
                     .text)
        c3yrqrank = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtC3yrqrank"})
                     .text)
        c5yrqrank = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtC5yrqrank"})
                     .text)
        c10yrqrank = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtC10yrqrank"})
                      .text)

        return {"fund_1month_return": fs1mthrtn,
                "fund_3month_return": fs3mthrtn,
                "fund_6month_return": fs6mthrtn,
                "fund_ytd_return": fsytdrtn,
                "fund_1year_return": fc1yrrtn,
                "fund_3year_return": fc3yrrtn,
                "fund_5year_return": fc5yrrtn,
                "fund_10year_return": fc10yrrtn,
                "benchmark_1month_return": is1mthrtn,
                "benchmark_3month_return": is3mthrtn,
                "benchmark_6month_return": is6mthrtn,
                "benchmark_ytd_return": isytdrtn,
                "benchmark_1year_return": ic1yrrtn,
                "benchmark_3year_return": ic3yrrtn,
                "benchmark_5year_return": ic5yrrtn,
                "benchmark_10year_return": ic10yrrtn,
                "quartile_rank__1month_return": s1mthqrank,
                "quartile_rank__3month_return": s3mthqrank,
                "quartile_rank__6month_return": s6mthqrank,
                "quartile_rank__ytd_return": sytdrank,
                "quartile_rank__1year_return": c1yrqrank,
                "quartile_rank__3year_return": c3yrqrank,
                "quartile_rank__5year_return": c5yrqrank,
                "quartile_rank__10year_return": c10yrqrank}


    def scrape_calendar_return(self):
        #pylint: disable-msg=too-many-locals
        """
        Extract calendar returns data from performance section at bottom of
        page.
        """
        # Fund
        calrtnyr1 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr1"})
                     .text)
        calrtnyr2 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr2"})
                     .text)
        calrtnyr3 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr3"})
                     .text)
        calrtnyr4 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr4"})
                     .text)
        calrtnyr5 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr5"})
                     .text)
        calrtnyr6 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr6"})
                     .text)
        calrtnyr7 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr7"})
                     .text)
        calrtnyr8 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr8"})
                     .text)
        calrtnyr9 = (self.soup
                     .find("span", {"id": "ctl00_MainContent_txtCalRtnyr9"})
                     .text)
        calrtnyr10 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtCalRtnyr10"})
                      .text)

        # Benchmark
        bcalrtnyr1 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr1"})
                      .text)
        bcalrtnyr2 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr2"})
                      .text)
        bcalrtnyr3 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr3"})
                      .text)
        bcalrtnyr4 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr4"})
                      .text)
        bcalrtnyr5 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr5"})
                      .text)
        bcalrtnyr6 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr6"})
                      .text)
        bcalrtnyr7 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr7"})
                      .text)
        bcalrtnyr8 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr8"})
                      .text)
        bcalrtnyr9 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr9"})
                      .text)
        bcalrtnyr10 = (self.soup
                       .find("span", {"id": "ctl00_MainContent_txtBCalRtnyr10"})
                       .text)

        # Quartile ranking
        qcalrtnyr1 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr1"})
                      .text)
        qcalrtnyr2 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr2"})
                      .text)
        qcalrtnyr3 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr3"})
                      .text)
        qcalrtnyr4 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr4"})
                      .text)
        qcalrtnyr5 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr5"})
                      .text)
        qcalrtnyr6 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr6"})
                      .text)
        qcalrtnyr7 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr7"})
                      .text)
        qcalrtnyr8 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr8"})
                      .text)
        qcalrtnyr9 = (self.soup
                      .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr9"})
                      .text)
        qcalrtnyr10 = (self.soup
                       .find("span", {"id": "ctl00_MainContent_txtQCalrtnyr10"})
                       .text)

        return {"fund_calendar_return_year_1": calrtnyr1,
                "fund_calendar_return_year_2": calrtnyr2,
                "fund_calendar_return_year_3": calrtnyr3,
                "fund_calendar_return_year_4": calrtnyr4,
                "fund_calendar_return_year_5": calrtnyr5,
                "fund_calendar_return_year_6": calrtnyr6,
                "fund_calendar_return_year_7": calrtnyr7,
                "fund_calendar_return_year_8": calrtnyr8,
                "fund_calendar_return_year_9": calrtnyr9,
                "fund_calendar_return_year_10": calrtnyr10,
                "benchmark_calendar_return_year_1": bcalrtnyr1,
                "benchmark_calendar_return_year_2": bcalrtnyr2,
                "benchmark_calendar_return_year_3": bcalrtnyr3,
                "benchmark_calendar_return_year_4": bcalrtnyr4,
                "benchmark_calendar_return_year_5": bcalrtnyr5,
                "benchmark_calendar_return_year_6": bcalrtnyr6,
                "benchmark_calendar_return_year_7": bcalrtnyr7,
                "benchmark_calendar_return_year_8": bcalrtnyr8,
                "benchmark_calendar_return_year_9": bcalrtnyr9,
                "benchmark_calendar_return_year_10": bcalrtnyr10,
                "quartile_rank_calendar_return_year_1": qcalrtnyr1,
                "quartile_rank_calendar_return_year_2": qcalrtnyr2,
                "quartile_rank_calendar_return_year_3": qcalrtnyr3,
                "quartile_rank_calendar_return_year_4": qcalrtnyr4,
                "quartile_rank_calendar_return_year_5": qcalrtnyr5,
                "quartile_rank_calendar_return_year_6": qcalrtnyr6,
                "quartile_rank_calendar_return_year_7": qcalrtnyr7,
                "quartile_rank_calendar_return_year_8": qcalrtnyr8,
                "quartile_rank_calendar_return_year_9": qcalrtnyr9,
                "quartile_rank_calendar_return_year_10": qcalrtnyr10}
