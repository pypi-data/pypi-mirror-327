from dataclasses import dataclass, field

import plotly.figure_factory as ff  # type: ignore
import plotly.graph_objects as go  # type: ignore
from loguru import logger  # type: ignore

from plottah.colors import PlotColors
from plottah.plots.plot_protocol import PlotProtocol
from plottah.utils import quantile_clipping, remove_or_impute_nan_infs


@dataclass
class DistPlot(PlotProtocol):
    # set the colorway
    colors: PlotColors = field(default_factory=lambda: PlotColors())

    # set hover setting
    hoverinfo: str = field(default_factory=lambda: "skip")

    # default to no quantile clipping
    distplot_q_min: float | None = field(default_factory=lambda: None)
    distplot_q_max: float | None = field(default_factory=lambda: None)

    # set default titles; can hide if not needed
    tick_font_size: int = field(default_factory=lambda: 10)
    title_font_size: int = field(default_factory=lambda: 12)

    def do_math(
        self,
        df,
        feature_col,
        target_col,
        fillna: bool = False,
    ):
        """
        does the required math to generate the traces, annotations and axes for the roc-curve plot

        1. imputes/removes missing values
        2. extract traces from the distplot function from plotly
        3. get the max density and feature value after imputing
        """

        logger.info("Started math for DistPlot")

        # 1. impute/remove missing values
        self.df_imputed = remove_or_impute_nan_infs(
            df.copy(), feature_col, target_col, fillna=fillna
        )

        # Optional - clip based on quantiles
        if (self.distplot_q_min is not None) or (self.distplot_q_max is not None):
            # if only min OR max provided, set other to limit
            if self.distplot_q_min is None:
                logger.warning(
                    f"{feature_col} only has distplot_q_max "
                    f"({self.distplot_q_max}) provided, "
                    f"so setting distplot_q_min to 0"
                )
                self.distplot_q_min = 0.0

            if self.distplot_q_max is None:
                logger.warning(
                    f"{feature_col} only has distplot_q_min "
                    f"({self.distplot_q_min}) provided, "
                    f"so setting distplot_q_max to 1"
                )
                self.distplot_q_max = 1.0

            # clip based on quantiles
            self.df_imputed = quantile_clipping(
                self.df_imputed, feature_col, self.distplot_q_min, self.distplot_q_max
            )

            # get the number of distinct feature values - must be at least 2
            distinct_values = min(
                self.df_imputed.loc[
                    (self.df_imputed[target_col] == 1), feature_col
                ].nunique(),
                self.df_imputed.loc[
                    (self.df_imputed[target_col] == 0), feature_col
                ].nunique(),
            )

            if distinct_values < 2:
                logger.warning(
                    f"One group of {feature_col} only has {distinct_values} distinct values, "
                    f"this will cause erors. Please revise the quantiles used for clipping"
                )

        # 2. extract traces from the distplot function from plotly
        self.hist_data = [
            self.df_imputed.loc[(self.df_imputed[target_col] == 0), feature_col].values,
            self.df_imputed.loc[(self.df_imputed[target_col] == 1), feature_col].values,
        ]

        self.group_labels = ["0", "1"]
        self.distplot = ff.create_distplot(self.hist_data, self.group_labels)

        # 3. get the max density and feature value after imputing
        self.max_density = max(
            self.distplot["data"][2].y.max(), self.distplot["data"][3].y.max()
        )
        self.max_val_adj = self.df_imputed[feature_col].max()

    def get_traces(self):
        return [
            # plot the first distribution:
            {
                "trace": go.Scatter(
                    self.distplot["data"][2],
                    line=dict(color=self.colors.get_rgba(), width=0.5),
                    fill="tonexty",
                    fillcolor=self.colors.get_rgba(opacity=0.2),
                    hoverinfo=self.hoverinfo,
                ),
                # share y
                "secondary_y": False,
            },
            # plot the second distribution
            {
                "trace": go.Scatter(
                    self.distplot["data"][3],
                    line=dict(color=self.colors.get_rgba("secondary_color"), width=0.5),
                    fill="tozeroy",
                    fillcolor=self.colors.get_rgba("secondary_color", opacity=0.2),
                    hoverinfo=self.hoverinfo,
                ),
                # share y
                "secondary_y": False,
            },
        ]

    def get_x_axes_layout(self, row, col):
        return dict(
            title_font={"size": self.title_font_size},
            tickfont={"size": self.tick_font_size},
        )

    def get_y_axes_layout(self, row, col):
        return dict(
            title_text="Density",
            title_font={"size": self.title_font_size},
            tickfont={"size": self.tick_font_size},
            row=row,
            col=col,
            title_standoff=5,  # decrease space between title and plot
        )

    def get_annotations(self, xref, yref):
        return [
            dict(
                x=0.9 * self.max_val_adj,
                y=1 * self.max_density,
                xref=xref,
                yref=yref,
                text="Class: 0",
                font=dict(color=self.colors.get_rgba()),
                showarrow=False,
                bordercolor="rgba(255,255,255,1)",
                borderwidth=2,
                borderpad=4,
                bgcolor="rgba(255,255,255,1)",
                opacity=0.8,
            ),
            dict(
                x=0.9 * self.max_val_adj,
                y=0.9 * self.max_density,
                xref=xref,
                yref=yref,
                text="Class: 1",
                font=dict(color=self.colors.get_rgba("secondary_color")),
                showarrow=False,
                bordercolor="rgba(255,255,255,1)",
                borderwidth=2,
                borderpad=4,
                bgcolor="rgba(255,255,255,1)",
                opacity=0.8,
            ),
        ]
