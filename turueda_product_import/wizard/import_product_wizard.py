# Copyright 2023 Camilo Prado
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
import base64
import uuid
from ast import literal_eval
from datetime import date, datetime as dt
from io import BytesIO

import xlrd
import xlwt

from odoo import _, fields, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class TuruedaProductImport(models.TransientModel):
    _name = "turueda.product.import"
    _description = "Turueda Product Import"

    import_file = fields.Binary(string="Import File (*.xlsx)")

    def action_import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()
        if self.import_file:
            self._import_record_data(self.import_file)
        else:
            raise ValidationError(_("Please select Excel file to import"))

    @api.model
    def _import_record_data(self, import_file):
        try:
            decoded_data = base64.decodebytes(import_file)
            book = xlrd.open_workbook(file_contents=decoded_data)
            sheet = book.sheet_by_index(0)
            product_attribute_carga = self._search_or_create_product_attribute('Carga')
            product_attribute_velocidad = self._search_or_create_product_attribute('Velocidad')
            product_attribute_marca = self._search_or_create_product_attribute('Marca')
            product_attribute_peso = self._search_or_create_product_attribute('Peso')
            product_attribute_diametro = self._search_or_create_product_attribute('Diámetro')
            product_attribute_anchura = self._search_or_create_product_attribute('Anchura')
            product_attribute_altura = self._search_or_create_product_attribute('Altura')
            product_attribute_tasa = self._search_or_create_product_attribute('Tasa')
            product_attribute_sonoridad = self._search_or_create_product_attribute('Eficiencia Sonoridad')
            product_attribute_consumo = self._search_or_create_product_attribute('Eficiencia Consumo')
            product_attribute_frenada = self._search_or_create_product_attribute('Eficiencia Frenada')
            product_attribute_temporada = self._search_or_create_product_attribute('Temporada')
            product_attribute_segmento = self._search_or_create_product_attribute('Segmento')


            for row in range(1, sheet.nrows):
                default_code = sheet.cell_value(row, 0)
                barcode = sheet.cell_value(row, 1)
                name = sheet.cell_value(row, 2)
                product_attribute_value_carga = sheet.cell_value(row, 3)
                product_attribute_value_velocidad = sheet.cell_value(row, 4)
                product_attribute_value_marca = sheet.cell_value(row, 5)
                product_attribute_value_peso = sheet.cell_value(row, 6)
                product_attribute_value_diametro = sheet.cell_value(row, 7)
                product_attribute_value_anchura = sheet.cell_value(row, 9)
                product_attribute_value_altura = sheet.cell_value(row, 10)
                product_attribute_value_tasa = sheet.cell_value(row, 11)
                product_attribute_value_sonoridad = sheet.cell_value(row, 12)
                product_attribute_value_consumo = sheet.cell_value(row, 13)
                product_attribute_value_frenada = sheet.cell_value(row, 14)
                product_attribute_value_temporada = sheet.cell_value(row, 16)
                product_attribute_value_segmento = sheet.cell_value(row, 17)
                description_sale = sheet.cell_value(row, 8)

                if not name:
                    return
                print("name", name)
                product_template = self._search_or_create_product_template(
                    default_code, barcode, name, description_sale
                )
                if not product_template:
                    return

                product_attribute_carga_value = self._search_or_create_product_attribute_value(
                    product_attribute_carga, product_attribute_value_carga
                )

                product_attribute_velocidad_value = self._search_or_create_product_attribute_value(
                    product_attribute_velocidad, product_attribute_value_velocidad
                )

                product_attribute_marca_value = self._search_or_create_product_attribute_value(
                    product_attribute_marca, product_attribute_value_marca
                )

                product_attribute_peso_value = self._search_or_create_product_attribute_value(
                    product_attribute_peso, product_attribute_value_peso
                )

                product_attribute_diametro_value = self._search_or_create_product_attribute_value(
                    product_attribute_diametro, product_attribute_value_diametro
                )

                product_attribute_anchura_value = self._search_or_create_product_attribute_value(
                    product_attribute_anchura, product_attribute_value_anchura
                )

                product_attribute_altura_value = self._search_or_create_product_attribute_value(
                    product_attribute_altura, product_attribute_value_altura
                )

                product_attribute_tasa_value = self._search_or_create_product_attribute_value(
                    product_attribute_tasa, product_attribute_value_tasa
                )

                product_attribute_sonoridad_value = self._search_or_create_product_attribute_value(
                    product_attribute_sonoridad, product_attribute_value_sonoridad
                )

                product_attribute_consumo_value = self._search_or_create_product_attribute_value(
                    product_attribute_consumo, product_attribute_value_consumo
                )

                product_attribute_frenada_value = self._search_or_create_product_attribute_value(
                    product_attribute_frenada, product_attribute_value_frenada
                )

                product_attribute_temporada_value = self._search_or_create_product_attribute_value(
                    product_attribute_temporada, product_attribute_value_temporada
                )

                product_attribute_segmento_value = self._search_or_create_product_attribute_value(
                    product_attribute_segmento, product_attribute_value_segmento
                )

                if product_attribute_carga_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_carga, product_attribute_carga_value
                    )

                if product_attribute_velocidad_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_velocidad, product_attribute_velocidad_value
                    )

                if product_attribute_marca_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_marca, product_attribute_marca_value
                    )

                if product_attribute_peso_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_peso, product_attribute_peso_value
                    )

                if product_attribute_diametro_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_diametro, product_attribute_diametro_value
                    )

                if product_attribute_anchura_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_anchura, product_attribute_anchura_value
                    )

                if product_attribute_altura_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_altura, product_attribute_altura_value
                    )

                if product_attribute_tasa_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_tasa, product_attribute_tasa_value
                    )

                if product_attribute_sonoridad_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_sonoridad, product_attribute_sonoridad_value
                    )

                if product_attribute_consumo_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_consumo, product_attribute_consumo_value
                    )

                if product_attribute_frenada_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_frenada, product_attribute_frenada_value
                    )

                if product_attribute_temporada_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_temporada, product_attribute_temporada_value
                    )

                if product_attribute_segmento_value:
                    self._search_or_create_product_template_attribute_line(
                        product_template, product_attribute_segmento, product_attribute_segmento_value
                    )

        except xlrd.XLRDError:
            raise ValidationError(
                _("Invalid file style, only .xls or .xlsx file allowed")
            )
        except Exception as e:
            raise e

    def _search_or_create_product_template(self, default_code, barcode, name, description_sale):
        result = self.env["product.template"].search([("name", "=", name)])
        if result:
            return result
        product_template = {
            'detailed_type': 'product',
            'invoice_policy': 'delivery',
            'default_code': default_code,
            'barcode': barcode,
            'name': name,
            'description_sale': description_sale,
        }

        # category_id = self._search_or_create_category(category)
        # if category_id:
        #     product_template['categ_id'] = category_id.id

        # product_tag_ids = self._search_or_create_product_tag(product_tag)
        # if product_tag_ids:
        #     product_template['product_tag_ids'] = [(6, 0, product_tag_ids.ids)]

        return self.env["product.template"].create(product_template)

    # def _search_or_create_category(self, category):
    #     if not category:
    #         return
    #     result = self.env["product.category"].search([("name", "=", category)])
    #     if result:
    #         return result
    #     return self.env["product.category"].create({"name": category})

    # def _search_or_create_product_tag(self, product_tag):
    #     if not product_tag:
    #         return
    #     result = self.env["product.tag"].search([("name", "=", product_tag)])
    #     if result:
    #         return result
    #     return self.env["product.tag"].create({"name": product_tag})

    def _search_or_create_product_attribute(self, product_attribute):
        result = self.env["product.attribute"].search([("name", "=", product_attribute)])
        if result:
            return result
        result = self.env["product.attribute"].create(
            {"name": product_attribute}
        )
        return result

    def _search_or_create_product_attribute_value(self, product_attribute, product_attribute_value):
        product_attribute_id = product_attribute[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_id),
                ("name", "=", product_attribute_value),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_id,
                "name": product_attribute_value,
            }
        )

    def _search_or_create_product_template_attribute_line(self, product_template, product_attribute, product_attribute_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute.id),
                ("value_ids", "in", product_attribute_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute.id),
            ]
        )
        if result and product_attribute_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute.id,
                "value_ids": [(6, 0, [product_attribute_value.id])],
            }
        )
        return result

