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

                product_attribute_carga_value = self._search_or_create_product_attribute_value_carga(
                    product_attribute_carga, product_attribute_value_carga
                )

                product_attribute_velocidad_value = self._search_or_create_product_attribute_value_velocidad(
                    product_attribute_velocidad, product_attribute_value_velocidad
                )

                product_attribute_marca_value = self._search_or_create_product_attribute_value_marca(
                    product_attribute_marca, product_attribute_value_marca
                )

                product_attribute_peso_value = self._search_or_create_product_attribute_value_peso(
                    product_attribute_peso, product_attribute_value_peso
                )

                product_attribute_diametro_value = self._search_or_create_product_attribute_value_diametro(
                    product_attribute_diametro, product_attribute_value_diametro
                )

                product_attribute_anchura_value = self._search_or_create_product_attribute_value_anchura(
                    product_attribute_anchura, product_attribute_value_anchura
                )

                product_attribute_altura_value = self._search_or_create_product_attribute_value_altura(
                    product_attribute_altura, product_attribute_value_altura
                )

                product_attribute_tasa_value = self._search_or_create_product_attribute_value_tasa(
                    product_attribute_tasa, product_attribute_value_tasa
                )

                product_attribute_sonoridad_value = self._search_or_create_product_attribute_value_sonoridad(
                    product_attribute_sonoridad, product_attribute_value_sonoridad
                )

                product_attribute_consumo_value = self._search_or_create_product_attribute_value_consumo(
                    product_attribute_consumo, product_attribute_value_consumo
                )

                product_attribute_frenada_value = self._search_or_create_product_attribute_value_frenada(
                    product_attribute_frenada, product_attribute_value_frenada
                )

                product_attribute_temporada_value = self._search_or_create_product_attribute_value_temporada(
                    product_attribute_temporada, product_attribute_value_temporada
                )

                product_attribute_segmento_value = self._search_or_create_product_attribute_value_segmento(
                    product_attribute_segmento, product_attribute_value_segmento
                )


                if not product_attribute_carga_value:
                    self._search_or_create_product_attribute_line_carga(
                        product_template, product_attribute_carga, product_attribute_carga_value
                    )

                if not product_attribute_velocidad_value:
                    self._search_or_create_product_attribute_line_velocidad(
                        product_template, product_attribute_velocidad, product_attribute_velocidad_value
                    )

                if not product_attribute_marca_value:
                    self._search_or_create_product_attribute_line_marca(
                        product_template, product_attribute_marca, product_attribute_marca_value
                    )

                if not product_attribute_peso_value:
                    self._search_or_create_product_attribute_line_peso(
                        product_template, product_attribute_peso, product_attribute_peso_value
                    )

                if not product_attribute_diametro_value:
                    self._search_or_create_product_attribute_line_diametro(
                        product_template, product_attribute_diametro, product_attribute_diametro_value
                    )

                if not product_attribute_anchura_value:
                    self._search_or_create_product_attribute_line_anchura(
                        product_template, product_attribute_anchura, product_attribute_anchura_value
                    )

                if not product_attribute_altura_value:
                    self._search_or_create_product_attribute_line_altura(
                        product_template, product_attribute_altura, product_attribute_altura_value
                    )

                if not product_attribute_tasa_value:
                    self._search_or_create_product_attribute_line_tasa(
                        product_template, product_attribute_tasa, product_attribute_tasa_value
                    )

                if not product_attribute_sonoridad_value:
                    self._search_or_create_product_attribute_line_sonoridad(
                        product_template, product_attribute_sonoridad, product_attribute_sonoridad_value
                    )

                if not product_attribute_consumo_value:
                    self._search_or_create_product_attribute_line_consumo(
                        product_template, product_attribute_consumo, product_attribute_consumo_value
                    )

                if not product_attribute_frenada_value:
                    self._search_or_create_product_attribute_line_frenada(
                        product_template, product_attribute_frenada, product_attribute_frenada_value
                    )

                if not product_attribute_temporada_value:
                    self._search_or_create_product_attribute_line_temporada(
                        product_template, product_attribute_temporada, product_attribute_temporada_value
                    )

                if not product_attribute_segmento_value:
                    self._search_or_create_product_attribute_line_segmento(
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

    def _search_or_create_product_attribute_value_carga(self, product_attribute_carga, product_attribute_value_carga):
        product_attribute_carga_id = product_attribute_carga[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_carga_id),
                ("name", "=", product_attribute_value_carga),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_carga_id,
                "name": product_attribute_value_carga,
            }
        )

    def _search_or_create_product_attribute_line_carga(self, product_template, product_attribute_carga,
                                                 product_attribute_carga_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_carga.id),
                ("value_ids", "in", product_attribute_carga_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_carga.id),
            ]
        )
        if result and product_attribute_carga_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_carga_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_carga.id,
                "value_ids": [(6, 0, [product_attribute_carga_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_velocidad(self, product_attribute_velocidad, product_attribute_value_velocidad):
        product_attribute_velocidad_id = product_attribute_velocidad[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_velocidad_id),
                ("name", "=", product_attribute_value_velocidad),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_velocidad_id,
                "name": product_attribute_value_velocidad,
            }
        )

    def _search_or_create_product_attribute_line_velocidad(self, product_template, product_attribute_velocidad,
                                                 product_attribute_velocidad_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_velocidad.id),
                ("value_ids", "in", product_attribute_velocidad_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_velocidad.id),
            ]
        )
        if result and product_attribute_velocidad_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_velocidad_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_velocidad.id,
                "value_ids": [(6, 0, [product_attribute_velocidad_value.id])],
            }
        )
        return result
    def _search_or_create_product_attribute_value_marca(self, product_attribute_marca, product_attribute_value_marca):
        product_attribute_marca_id = product_attribute_marca[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_marca_id),
                ("name", "=", product_attribute_value_marca),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_marca_id,
                "name": product_attribute_value_marca,
            }
        )

    def _search_or_create_product_attribute_line_marca(self, product_template, product_attribute_marca,
                                                 product_attribute_marca_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_marca.id),
                ("value_ids", "in", product_attribute_marca_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_marca.id),
            ]
        )
        if result and product_attribute_marca_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_marca_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_marca.id,
                "value_ids": [(6, 0, [product_attribute_marca_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_peso(self, product_attribute_peso, product_attribute_value_peso):
        product_attribute_peso_id = product_attribute_peso[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_peso_id),
                ("name", "=", product_attribute_value_peso),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_peso_id,
                "name": product_attribute_value_peso,
            }
        )

    def _search_or_create_product_attribute_line_peso(self, product_template, product_attribute_peso,
                                                 product_attribute_peso_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_peso.id),
                ("value_ids", "in", product_attribute_peso_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_peso.id),
            ]
        )
        if result and product_attribute_peso_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_peso_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_peso.id,
                "value_ids": [(6, 0, [product_attribute_peso_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_diametro(self, product_attribute_diametro, product_attribute_value_diametro):
        product_attribute_diametro_id = product_attribute_diametro[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_diametro_id),
                ("name", "=", product_attribute_value_diametro),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_diametro_id,
                "name": product_attribute_value_diametro,
            }
        )

    def _search_or_create_product_attribute_line_diametro(self, product_template, product_attribute_diametro,
                                                 product_attribute_diametro_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_diametro.id),
                ("value_ids", "in", product_attribute_diametro_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_diametro.id),
            ]
        )
        if result and product_attribute_diametro_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_diametro_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_diametro.id,
                "value_ids": [(6, 0, [product_attribute_diametro_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_anchura(self, product_attribute_anchura, product_attribute_value_anchura):
        product_attribute_anchura_id = product_attribute_anchura[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_anchura_id),
                ("name", "=", product_attribute_value_anchura),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_anchura_id,
                "name": product_attribute_value_anchura,
            }
        )

    def _search_or_create_product_attribute_line_anchura(self, product_template, product_attribute_anchura,
                                                 product_attribute_anchura_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_anchura.id),
                ("value_ids", "in", product_attribute_anchura_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_anchura.id),
            ]
        )
        if result and product_attribute_anchura_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_anchura_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_anchura.id,
                "value_ids": [(6, 0, [product_attribute_anchura_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_altura(self, product_attribute_altura, product_attribute_value_altura):
        product_attribute_altura_id = product_attribute_altura[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_altura_id),
                ("name", "=", product_attribute_value_altura),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_altura_id,
                "name": product_attribute_value_altura,
            }
        )

    def _search_or_create_product_attribute_line_altura(self, product_template, product_attribute_altura,
                                                 product_attribute_altura_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_altura.id),
                ("value_ids", "in", product_attribute_altura_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_altura.id),
            ]
        )
        if result and product_attribute_altura_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_altura_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_altura.id,
                "value_ids": [(6, 0, [product_attribute_altura_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_tasa(self, product_attribute_tasa, product_attribute_value_tasa):
        product_attribute_tasa_id = product_attribute_tasa[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_tasa_id),
                ("name", "=", product_attribute_value_tasa),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_tasa_id,
                "name": product_attribute_value_tasa,
            }
        )

    def _search_or_create_product_attribute_line_tasa(self, product_template, product_attribute_tasa,
                                                 product_attribute_tasa_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_tasa.id),
                ("value_ids", "in", product_attribute_tasa_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_tasa.id),
            ]
        )
        if result and product_attribute_tasa_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_tasa_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_tasa.id,
                "value_ids": [(6, 0, [product_attribute_tasa_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_sonoridad(self, product_attribute_sonoridad, product_attribute_value_sonoridad):
        product_attribute_sonoridad_id = product_attribute_sonoridad[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_sonoridad_id),
                ("name", "=", product_attribute_value_sonoridad),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_sonoridad_id,
                "name": product_attribute_value_sonoridad,
            }
        )

    def _search_or_create_product_attribute_line_sonoridad(self, product_template, product_attribute_sonoridad,
                                                 product_attribute_sonoridad_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_sonoridad.id),
                ("value_ids", "in", product_attribute_sonoridad_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_sonoridad.id),
            ]
        )
        if result and product_attribute_sonoridad_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_sonoridad_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_sonoridad.id,
                "value_ids": [(6, 0, [product_attribute_sonoridad_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_consumo(self, product_attribute_consumo, product_attribute_value_consumo):
        product_attribute_consumo_id = product_attribute_consumo[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_consumo_id),
                ("name", "=", product_attribute_value_consumo),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_consumo_id,
                "name": product_attribute_value_consumo,
            }
        )

    def _search_or_create_product_attribute_line_consumo(self, product_template, product_attribute_consumo,
                                                 product_attribute_consumo_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_consumo.id),
                ("value_ids", "in", product_attribute_consumo_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_consumo.id),
            ]
        )
        if result and product_attribute_consumo_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_consumo_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_consumo.id,
                "value_ids": [(6, 0, [product_attribute_consumo_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_frenada(self, product_attribute_frenada, product_attribute_value_frenada):
        product_attribute_frenada_id = product_attribute_frenada[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_frenada_id),
                ("name", "=", product_attribute_value_frenada),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_frenada_id,
                "name": product_attribute_value_frenada,
            }
        )

    def _search_or_create_product_attribute_line_frenada(self, product_template, product_attribute_frenada,
                                                 product_attribute_frenada_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_frenada.id),
                ("value_ids", "in", product_attribute_frenada_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_frenada.id),
            ]
        )
        if result and product_attribute_frenada_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_frenada_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_frenada.id,
                "value_ids": [(6, 0, [product_attribute_frenada_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_temporada(self, product_attribute_temporada, product_attribute_value_temporada):
        product_attribute_temporada_id = product_attribute_temporada[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_temporada_id),
                ("name", "=", product_attribute_value_temporada),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_temporada_id,
                "name": product_attribute_value_temporada,
            }
        )

    def _search_or_create_product_attribute_line_temporada(self, product_template, product_attribute_temporada,
                                                 product_attribute_temporada_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_temporada.id),
                ("value_ids", "in", product_attribute_temporada_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_temporada.id),
            ]
        )
        if result and product_attribute_temporada_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_temporada_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_temporada.id,
                "value_ids": [(6, 0, [product_attribute_temporada_value.id])],
            }
        )
        return result

    def _search_or_create_product_attribute_value_segmento(self, product_attribute_segmento, product_attribute_value_segmento):
        product_attribute_segmento_id = product_attribute_segmento[0].id
        result = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", product_attribute_segmento_id),
                ("name", "=", product_attribute_value_segmento),
            ]
        )
        if result:
            return result
        return self.env["product.attribute.value"].create(
            {
                "attribute_id": product_attribute_segmento_id,
                "name": product_attribute_value_segmento,
            }
        )

    def _search_or_create_product_attribute_line_segmento(self, product_template, product_attribute_segmento,
                                                 product_attribute_segmento_value):
        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_segmento.id),
                ("value_ids", "in", product_attribute_segmento_value.id),
            ]
        )
        if result:
            return result

        result = self.env["product.template.attribute.line"].search(
            [
                ("product_tmpl_id", "=", product_template.id),
                ("attribute_id", "=", product_attribute_segmento.id),
            ]
        )
        if result and product_attribute_segmento_value not in result.value_ids:
            result.write({
                "value_ids": [(4, product_attribute_segmento_value.id)]
            })
            return result

        result = self.env["product.template.attribute.line"].create(
            {
                "product_tmpl_id": product_template.id,
                "attribute_id": product_attribute_segmento.id,
                "value_ids": [(6, 0, [product_attribute_segmento_value.id])],
            }
        )
        return result
