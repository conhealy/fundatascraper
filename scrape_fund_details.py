#pylint: disable-msg=too-many-locals
"""
Program that scrapes details of mutual funds from fundata website.
"""
import time
from random import randint
import pandas as pd
from fundatascraper import fundlist
from fundatascraper.fund_page import FundProfileScraper

def main():
    """ Scrape details of all mutual funds listed on fundata.com """
    href_list = fundlist.get_fund_list()

    single_values = None
    asset_allocations = None
    geo_allocations = None
    sector_allocations = None
    top10_holdings = None

    for href in href_list:
        url = 'http://idata.fundata.com' + href
        fund_profile = FundProfileScraper(url)

        value_dict = fund_profile.scrape_all_single_value()
        if single_values is None:
            single_values = pd.DataFrame([value_dict.values()],
                                         columns=value_dict.keys())
        else:
            temp_df = pd.DataFrame(value_dict.values(),
                                   columns=value_dict.keys())
            single_values.append(temp_df)

        asset_allocation_list = fund_profile.scrape_asset_allocation()
        allocations_with_href = [[href, asset_class]
                                 for asset_class in asset_allocation_list]
        if asset_allocations is None:
            asset_allocations = pd.DataFrame(
                allocations_with_href,
                columns=['href', 'asset_allocation']
            )
        else:
            temp_df = pd.DataFrame(
                allocations_with_href,
                columns=['href', 'asset_allocation']
            )
            asset_allocations.append(temp_df)


        geo_allocations_list = fund_profile.scrape_geo_allocation()
        geo_allocations_href = [[href, geo_class]
                                for geo_class in geo_allocations_list]
        if geo_allocations is None:
            geo_allocations = pd.DataFrame(
                geo_allocations_href,
                columns=['href', 'geo_allocation']
            )
        else:
            temp_df = pd.DataFrame(
                geo_allocations_href,
                columns=['href', 'geo_allocation']
            )
            geo_allocations.append(temp_df)

        sector_allocations_list = fund_profile.scrape_sector_allocation()
        sector_allocations_href = [[href, sector_class]
                                   for sector_class in sector_allocations_list]
        if sector_allocations is None:
            sector_allocations = pd.DataFrame(
                sector_allocations_href,
                columns=['href', 'sector_allocation']
            )
        else:
            temp_df = pd.DataFrame(
                sector_allocations_href,
                columns=['href', 'sector_allocation']
            )
            sector_allocations.append(temp_df)

        top10_holding_list = fund_profile.scrape_top10_holdings()
        top10_holding_href = [[href, holding]
                              for holding in top10_holding_list]
        if top10_holdings is None:
            top10_holdings = pd.DataFrame(
                top10_holding_href,
                columns=['href', 'holding']
            )
        else:
            temp_df = pd.DataFrame(
                top10_holding_href,
                columns=['href', 'holding']
            )
            top10_holdings.append(temp_df)

        time.sleep(randint(1, 5))

    single_values.to_pickle('./single_values.pkl')
    asset_allocations.to_pickle('./asset_allocations.pkl')
    geo_allocations.to_pickle('./geo_allocations.pkl')
    sector_allocations.to_pickle('sector_allocations.pkl')
    top10_holdings.to_pickle('top10_holdings.pkl')


if __name__ == "__main__":
    main()
