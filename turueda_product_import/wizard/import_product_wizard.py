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
            for row in range(1, sheet.nrows):
                default_code = sheet.cell_value(row, 0)
                barcode = sheet.cell_value(row, 1)
                name = sheet.cell_value(row, 2)
                # product_attribute_value_carga = sheet.cell_value(row, 3)
                # product_attribute_value_velocidad = sheet.cell_value(row, 4)
                description_sale = sheet.cell_value(row, 8)
                # product_tag = sheet.cell_value(row, 5)
                # category = sheet.cell_value(row, 4)
                if not name:
                    return
                print("name", name)
                product_template = self._search_or_create_product_template(
                    default_code, barcode, name, description_sale
                )
                if not product_template:
                    return

                # product_attribute_color_value = self._search_or_create_product_attribute_value(
                #     product_attribute_color, product_attribute_value
                # )
                # if not product_attribute_color_value:
                #     self._search_or_create_product_attribute_line(
                #         product_template, product_attribute_color, product_attribute_color_value
                #     )

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

    # def _search_or_create_product_attribute_value(self, product_attribute_color, product_attribute_value):
    #     product_attribute_color_id = product_attribute_color[0].id
    #     result = self.env["product.attribute.value"].search(
    #         [
    #             ("attribute_id", "=", product_attribute_color_id),
    #             ("name", "=", product_attribute_value),
    #         ]
    #     )
    #     if result:
    #         return result
    #     return self.env["product.attribute.value"].create(
    #         {
    #             "attribute_id": product_attribute_color_id,
    #             "name": product_attribute_value,
    #         }
    #     )

    # def _search_or_create_product_attribute_line(self, product_template, product_attribute_color, product_attribute_color_value):
    #     result = self.env["product.template.attribute.line"].search(
    #         [
    #             ("product_tmpl_id", "=", product_template.id),
    #             ("attribute_id", "=", product_attribute_color.id),
    #             ("value_ids", "in", product_attribute_color_value.id),
    #         ]
    #     )
    #     if result:
    #         return result
    #     return self.env["product.template.attribute.line"].create(
    #         {
    #             "product_tmpl_id": product_template.id,
    #             "attribute_id": product_attribute_color.id,
    #             "value_ids": [(6, 0, [product_attribute_color_value.id])],
    #         }
    #     )
