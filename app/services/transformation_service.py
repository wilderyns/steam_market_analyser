from app.models.appstate import AppState


def to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def active_dataset(state: AppState):
    if state.dataset is None:
        raise RuntimeError("Dataset not loaded")
    return state.dataset


def detached_copy(dataset):
    if hasattr(dataset, "df"):
        return dataset.__class__(dataset.df.copy(deep=True))

    if hasattr(dataset, "_columns") and hasattr(dataset, "rows"):
        columns = list(dataset._columns)
        rows = [list(row) for row in dataset.rows]
        return dataset.__class__(columns, rows)

    return dataset


def ensure_transform_dataset(state: AppState):
    if state.base_dataset is None:
        raise RuntimeError("Base dataset not loaded")

    if state.transformations_applied:
        if state.dataset is None:
            raise RuntimeError("Transformed dataset is unavailable")
        return state.dataset

    filtered = state.base_dataset.filter(state.filters)
    transformed = detached_copy(filtered)
    state.dataset = transformed
    state.last_results = transformed
    state.transformations_applied = True
    state.transform_filter_note = "Transformations are running on the currently filtered dataset"
    return transformed


def clear_transformations(state: AppState) -> None:
    if state.base_dataset is None:
        raise RuntimeError("Base dataset not loaded")

    state.dataset = state.base_dataset
    state.last_results = state.base_dataset
    state.transformations_applied = False
    state.transform_filter_note = None


def transform_create_count(state: AppState, source_column: str, seperator: str | None, new_column_name: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)
    dataset.transform_create_count(new_column_name, source_column, seperator, overwrite=overwrite)


def transform_create_log(state: AppState, source_column: str, new_column: str, overwrite: bool = False) -> None:
    if not state.features.has_numpy:
        raise RuntimeError("NumPy is required for log transforms")

    dataset = ensure_transform_dataset(state)
    dataset.transform_create_log(source_column, new_column, overwrite=overwrite)


def transform_create_minmax(state: AppState, source_column: str, new_column: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)
    dataset.transform_create_minmax(source_column, new_column, overwrite=overwrite)


def transform_create_zscore(state: AppState, source_column: str, new_column: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)
    dataset.transform_create_zscore(source_column, new_column, overwrite=overwrite)


def create_sum_column(state: AppState, column1: str, column2: str, new_column: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)
    dataset.transform_column_combine(column1, column2, new_column, overwrite=overwrite)


def create_ratio_of_sum(state: AppState, column_x: str, column_y: str, new_column: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)

    pairs = dataset.get_column_values([column_x, column_y])
    values: list[float] = []

    for row in pairs:
        x = to_float(row[0])
        y = to_float(row[1])
        total = x + y
        if total <= 0:
            values.append(0.0)
        else:
            values.append(x / total)

    dataset.create_new_column(new_column, values, overwrite=overwrite)


def create_composite_three_column(state: AppState, column_x: str, column_y: str, column_z: str, new_column: str, overwrite: bool = False) -> None:
    dataset = ensure_transform_dataset(state)
    rows = dataset.get_column_values([column_x, column_y, column_z])

    values: list[float] = []
    for row in rows:
        x = to_float(row[0])
        y = to_float(row[1])
        z = to_float(row[2])
        if z == 0:
            values.append(0.0)
        else:
            values.append((x + y) / z)

    dataset.create_new_column(new_column, values, overwrite=overwrite)


def descriptive_statistics(state: AppState, columns: list[str]):
    dataset = active_dataset(state)

    headers = ["Column", "Count", "Mean", "Median", "Min", "Q1", "Q3", "Max", "Std"]
    rows: list[list] = []

    for column in columns:
        values = dataset.get_column_values([column])
        numbers: list[float] = []
        for value_row in values:
            value = value_row[0]
            try:
                numbers.append(float(value))
            except (TypeError, ValueError):
                continue

        if not numbers:
            rows.append([column, 0, "-", "-", "-", "-", "-", "-", "-"])
            continue

        ordered = sorted(numbers)
        count = len(ordered)
        mean_value = sum(ordered) / count

        def percentile(p: float) -> float:
            if count == 1:
                return ordered[0]
            index = (count - 1) * p
            lower = int(index)
            upper = min(lower + 1, count - 1)
            fraction = index - lower
            return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction

        median = percentile(0.5)
        q1 = percentile(0.25)
        q3 = percentile(0.75)
        variance = sum((x - mean_value) ** 2 for x in ordered) / count
        std_dev = variance ** 0.5

        rows.append([
            column,
            count,
            round(mean_value, 4),
            round(median, 4),
            round(min(ordered), 4),
            round(q1, 4),
            round(q3, 4),
            round(max(ordered), 4),
            round(std_dev, 4),
        ])

    return headers, rows


def grouped_average(state: AppState, group_column: str, value_column: str):
    dataset = active_dataset(state)

    values = dataset.get_column_values([group_column, value_column])
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}

    for row in values:
        group_name = str(row[0]) if row[0] is not None else ""
        try:
            value = float(row[1])
        except (TypeError, ValueError):
            continue

        totals[group_name] = totals.get(group_name, 0.0) + value
        counts[group_name] = counts.get(group_name, 0) + 1

    rows: list[list] = []
    for group_name in totals:
        avg = totals[group_name] / counts[group_name]
        rows.append([group_name, counts[group_name], round(avg, 4)])

    rows.sort(key=lambda r: r[2], reverse=True)
    return [group_column, "Count", f"Avg {value_column}"], rows


def top_n_rows(state: AppState, rank_column: str, n: int):
    dataset = active_dataset(state)

    all_columns = dataset.columns()
    rank_rows = dataset.get_column_values([rank_column])
    indexed: list[tuple[int, float]] = []

    for idx, row in enumerate(rank_rows):
        try:
            score = float(row[0])
        except (TypeError, ValueError):
            continue
        indexed.append((idx, score))

    indexed.sort(key=lambda x: x[1], reverse=True)
    top_indexes = [i for i, _ in indexed[:n]]

    full_rows = dataset.get_page(1, dataset.row_count())
    output_rows: list[list] = []
    for idx in top_indexes:
        if idx < len(full_rows):
            output_rows.append(full_rows[idx])

    return all_columns, output_rows


def string_list_value_ranking(state: AppState, list_column: str, seperator: str, top_n: int, score_column: str | None = None):
    dataset = active_dataset(state)

    columns = [list_column]
    if score_column:
        columns.append(score_column)

    values = dataset.get_column_values(columns)
    counts: dict[str, int] = {}
    score_totals: dict[str, float] = {}
    score_counts: dict[str, int] = {}

    for row in values:
        raw_items = str(row[0]) if row[0] is not None else ""
        if not raw_items:
            continue

        items = [item.strip() for item in raw_items.split(seperator) if item.strip()]
        for item in items:
            counts[item] = counts.get(item, 0) + 1

            if score_column:
                try:
                    score_value = float(row[1])
                except (TypeError, ValueError):
                    continue
                score_totals[item] = score_totals.get(item, 0.0) + score_value
                score_counts[item] = score_counts.get(item, 0) + 1

    rows: list[list] = []
    if score_column:
        for item, count in counts.items():
            avg = 0.0
            if score_counts.get(item, 0) > 0:
                avg = score_totals[item] / score_counts[item]
            rows.append([item, count, round(avg, 4)])
        rows.sort(key=lambda r: (r[1], r[2]), reverse=True)
        return ["Value", "Count", f"Avg {score_column}"], rows[:top_n]

    for item, count in counts.items():
        rows.append([item, count])
    rows.sort(key=lambda r: r[1], reverse=True)
    return ["Value", "Count"], rows[:top_n]
