from odoo import fields, models
from datetime import date, timedelta
import requests


class ResCurrencyRateProviderVCB(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("VCB", "Vietcombank")],
        ondelete={"VCB": "set default"},
        default="VCB",
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "VCB":
            return super()._get_supported_currencies()

        # Currencies rate available in VCB
        return ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'SGD', 'THB', 'CAD',
                'CHF', 'HKD', 'CNY', 'DKK', 'INR', 'KRW', 'KWD', 'MYR',
                'NOK', 'RUB', 'SAR', 'SEK', 'VND']

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if not self.service == "VCB":
            return super()._obtain_rates(
                base_currency=base_currency, currencies=currencies,
                date_from=date_from, date_to=date_to
            )

        # Request data from VCB
        url = "https://www.vietcombank.com.vn/api/exchangerates?date={rate_date}"

        # Ensure that date is not future
        date_to = date_to <= date.today() and date_to or date.today()
        date_from = date_from <= date.today() and date_from or date.today()

        # If the base currency is not VND, we need to add it in the list
        # To get data and re-calculate the rate later
        if base_currency != "VND" and base_currency not in currencies:
            currencies.append(base_currency)

        supported_currency_codes = self._get_supported_currencies()
        currencies = [currency for currency in currencies if currency.upper(
        ) in supported_currency_codes]

        res = {}
        while date_from <= date_to:
            res[date_from] = {}
            response = requests.get(url.format(
                rate_date=date_from.strftime("%Y-%m-%d")))
            response.raise_for_status()
            vcb_data = response.json().get("Data", [])

            for currency_code in currencies:
                if currency_code == "VND":
                    res[date_from][currency_code] = 1.0
                    continue

                for vcb_line in vcb_data:
                    if currency_code.upper() == vcb_line["currencyCode"].upper():
                        res[date_from][currency_code] = float(
                            vcb_line["transfer"])
                        break
            date_from += timedelta(days=1)

        if base_currency == "VND":
            return res

        for rate_date, currencies in res.items():
            base_rate = [
                res[rate_date][code]
                for code in res[rate_date] if code.upper() == base_currency.upper()]
            base_rate = base_rate[0]
            for currency_code in currencies:
                res[rate_date][currency_code] = base_rate / \
                    res[rate_date][currency_code]
        return res
