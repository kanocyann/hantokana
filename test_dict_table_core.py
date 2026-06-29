import unittest

from hantokana_app.dict_table_core import (
    calculate_scroll_max,
    calculate_table_scroll_max,
    calculate_table_size,
    constrain_resized_column_widths,
    format_selected_cells_as_tsv,
    ratio_column_widths,
)


class DictTableCoreTests(unittest.TestCase):
    def test_calculate_table_size_applies_margins_and_min_height(self):
        self.assertEqual(calculate_table_size(1100, 800), (1052, 560))
        self.assertEqual(calculate_table_size(20, 100), (0, 450))

    def test_ratio_column_widths_assigns_remainder_to_last_column(self):
        self.assertEqual(ratio_column_widths(1000), [450, 450, 100])
        self.assertEqual(ratio_column_widths(0), [0, 0, 0])

    def test_calculate_scroll_max_clamps_negative_values(self):
        self.assertEqual(calculate_scroll_max(100, 20, 300), 0)
        self.assertEqual(calculate_scroll_max(500, 30, 200, padding=5, extra_buffer=40), 375)

    def test_calculate_table_scroll_max_uses_visible_page_row_heights(self):
        self.assertEqual(calculate_table_scroll_max([30] * 10, 240, bottom_padding=8), 68)
        self.assertEqual(calculate_table_scroll_max([30] * 20, 240, bottom_padding=8), 368)
        self.assertEqual(calculate_table_scroll_max([80, 30, 30], 200, bottom_padding=8), 0)

    def test_constrain_resized_column_widths_clamps_requested_column(self):
        widths = constrain_resized_column_widths(900, [300, 300, 300], 0, 700)
        self.assertEqual(widths, [540, 300, 300])

    def test_constrain_resized_column_widths_preserves_minimums(self):
        widths = constrain_resized_column_widths(360, [80, 80, 80], 1, 20)
        self.assertEqual(widths, [150, 150, 150])

    def test_format_selected_cells_as_tsv_preserves_grid_shape(self):
        selected_cells = {
            (0, 0): "学校",
            (0, 2): "普通词",
            (1, 1): "しゅっちょう",
        }

        self.assertEqual(
            format_selected_cells_as_tsv(selected_cells),
            "学校\t\t普通词\n\tしゅっちょう\t",
        )

    def test_format_selected_cells_as_tsv_handles_empty_and_none_values(self):
        self.assertEqual(format_selected_cells_as_tsv({}), "")
        self.assertEqual(format_selected_cells_as_tsv({(0, 0): None, (0, 1): 0}), "\t0")


if __name__ == "__main__":
    unittest.main()
