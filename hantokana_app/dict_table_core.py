DEFAULT_COLUMN_RATIOS = (0.45, 0.45, 0.10)
DEFAULT_MIN_TABLE_HEIGHT = 450
DEFAULT_TABLE_MARGIN_H = 48
DEFAULT_TABLE_MARGIN_V = 240
DEFAULT_MIN_ROW_HEIGHT = 42
DEFAULT_SCROLL_BOTTOM_PADDING = 24


def calculate_table_size(
    window_width,
    window_height,
    margins_h=DEFAULT_TABLE_MARGIN_H,
    margins_v=DEFAULT_TABLE_MARGIN_V,
    min_height=DEFAULT_MIN_TABLE_HEIGHT,
):
    table_width = max(0, int(window_width) - margins_h)
    table_height = max(min_height, int(window_height) - margins_v)
    return table_width, table_height


def ratio_column_widths(available_width, ratios=DEFAULT_COLUMN_RATIOS):
    available_width = max(0, int(available_width))
    if not ratios:
        return []

    widths = []
    used_width = 0
    for ratio in ratios[:-1]:
        width = max(0, int(available_width * ratio))
        widths.append(width)
        used_width += width

    widths.append(max(0, available_width - used_width))
    return widths


def calculate_scroll_max(total_row_height, header_height, viewport_height, padding=0, extra_buffer=0):
    value = (
        int(total_row_height)
        + int(header_height)
        + int(padding)
        - int(viewport_height)
        + int(extra_buffer)
    )
    return max(0, value)


def calculate_table_scroll_max(row_heights, viewport_height, bottom_padding=DEFAULT_SCROLL_BOTTOM_PADDING):
    total_row_height = sum(max(0, int(height)) for height in row_heights)
    return calculate_scroll_max(
        total_row_height,
        0,
        viewport_height,
        extra_buffer=bottom_padding,
    )


def format_selected_cells_as_tsv(selected_cells):
    if not selected_cells:
        return ""

    rows = sorted({row for row, _col in selected_cells})
    cols = sorted({col for _row, col in selected_cells})

    lines = []
    for row in rows:
        row_texts = []
        for col in cols:
            value = selected_cells.get((row, col), "")
            row_texts.append("" if value is None else str(value))
        lines.append("\t".join(row_texts))
    return "\n".join(lines)


def constrain_resized_column_widths(
    total_width,
    column_widths,
    index,
    requested_width,
    min_width=150,
    max_width_ratio=0.6,
):
    widths = [int(width) for width in column_widths]
    if not widths or index < 0 or index >= len(widths):
        return widths

    total_width = max(0, int(total_width))
    requested_width = int(requested_width)
    min_width = max(0, int(min_width))

    max_allowed_width = total_width - min_width * (len(widths) - 1)
    max_width = min(max_allowed_width, int(total_width * max_width_ratio))
    max_width = max(max_width, min_width)

    if requested_width < min_width:
        widths[index] = min_width
    elif requested_width > max_width:
        widths[index] = max_width
    else:
        widths[index] = requested_width

    other_columns = [col for col in range(len(widths)) if col != index]
    remaining_width = total_width - widths[index]
    if remaining_width < min_width * len(other_columns):
        max_current_width = total_width - min_width * len(other_columns)
        if max_current_width >= min_width:
            widths[index] = max_current_width
        else:
            return [min_width for _ in widths]

    for col in other_columns:
        widths[col] = max(widths[col], min_width)

    return widths
