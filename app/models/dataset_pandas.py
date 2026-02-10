from app.models.dataset import Dataset, Row
from app.models.filters import Filters


class DatasetPandas(Dataset):
    def __init__(self, df):
        self.df = df

    def columns(self) -> list[str]:
        return [str(c) for c in self.df.columns.tolist()]

    def row_count(self) -> int:
        return int(len(self.df))

    def filter(self, filters: Filters) -> "DatasetPandas":
        import pandas

        dataframe = self.df

        if filters.year_min is not None or filters.year_max is not None:
            for col in ("Release date", "release_date", "ReleaseDate"):
                if col in dataframe.columns:
                    years = dataframe[col].astype(str).str.extract(r"(\d{4})", expand=False)
                    years = pandas.to_numeric(years, errors="coerce")
                    if filters.year_min is not None:
                        dataframe = dataframe[years >= filters.year_min]
                        years = years[years >= filters.year_min]
                    if filters.year_max is not None:
                        dataframe = dataframe[years <= filters.year_max]
                    break

        if filters.price_min is not None or filters.price_max is not None:
            for col in ("Price", "price"):
                if col in dataframe.columns:
                    prices = pandas.to_numeric(dataframe[col], errors="coerce")
                    if filters.price_min is not None:
                        dataframe = dataframe[prices >= filters.price_min]
                        prices = prices[prices >= filters.price_min]
                    if filters.price_max is not None:
                        dataframe = dataframe[prices <= filters.price_max]
                    break

        if filters.genre_contains:
            for col in ("Genres", "genres", "Tags", "tags"):
                if col in dataframe.columns:
                    dataframe = dataframe[dataframe[col].astype(str).str.contains(filters.genre_contains, case=False, na=False)]
                    break

        if filters.min_review_score is not None:
            for col in ("User score", "user_score", "Review score", "review_score"):
                if col in dataframe.columns:
                    scores = pandas.to_numeric(dataframe[col], errors="coerce")
                    dataframe = dataframe[scores >= filters.min_review_score]
                    break

        if filters.min_reviews is not None:
            for col in ("Recommendations", "recommendations", "Positive", "positive"):
                if col in dataframe.columns:
                    reviews = pandas.to_numeric(dataframe[col], errors="coerce")
                    dataframe = dataframe[reviews >= filters.min_reviews]
                    break

        return DatasetPandas(dataframe)

    def get_page(self, page: int, page_size: int) -> list[Row]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 1
        start = (page - 1) * page_size
        end = start + page_size
        rows: list[Row] = []
        for _, row in self.df.iloc[start:end].iterrows():
            rows.append([value.item() if hasattr(value, "item") else value for value in row.tolist()])
        return rows
