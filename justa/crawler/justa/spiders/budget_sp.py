import io

import rows

from justa.spiders.budget_base import BaseBudgetExecutionSpider, BRDecimalField


class SaoPauloBudgetExecutionSpider(BaseBudgetExecutionSpider):
    name = "budget_sp"
    state = "SP"
    url = "https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/FlexConsDespesa.aspx"
    value_to_wait_for = "Pesquisar"

    def select_year(self, year):
        select = self.browser.find_by_xpath("//select[contains(@name, 'Ano')]").first
        select.select_by_text(str(year))
        self.wait()

    def check_all_phases(self):
        finished = False
        while not finished:
            finished = True
            for checkbox in self.browser.find_by_xpath(
                "//input[@type='checkbox' and contains(@name, 'Fase')]"
            ):
                if not checkbox.checked:
                    checkbox.check()
                    self.wait()
                    finished = False
                    break

    def select_action(self, action):
        actions = self.browser.find_by_xpath(
            "//select[contains(@name, 'Acao')]/option[starts-with(@value, '{}')]".format(
                action
            )
        )
        assert len(actions) == 1
        select_action = self.browser.find_by_xpath(
            "//select[contains(@name, 'Acao')]"
        ).first
        action_text = actions.first.text
        select_action.select_by_text(action_text)
        self.wait()

    def do_search(self):
        self.browser.find_by_value("Pesquisar").first.click()
        self.wait()

    def parse_budget(self):
        table = rows.import_from_html(
            io.BytesIO(self.browser.html.encode("utf-8")),
            index=10,
            force_types={
                "dotacao_inicial": BRDecimalField,
                "dotacao_atual": BRDecimalField,
                "empenhado": BRDecimalField,
                "liquidado": BRDecimalField,
                "pago": BRDecimalField,
                "pago_restos": BRDecimalField,
            },
        )

        result = [row._asdict() for row in table if row.elemento != "TOTAL"]
        return rows.import_from_dicts(result)

    def execute(self, year, action):
        self.select_year(year)
        self.check_all_phases()
        self.select_action(action)
        self.do_search()
        for row in self.parse_budget():
            yield row._asdict()