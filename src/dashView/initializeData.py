from src.kMerAlignmentData import KMerAlignmentData
from src.kMerPCAData import KMerPCAData
from src.kMerScatterPlotData import KMerScatterPlotData
from src.processing import Processing
import src.layout.plot_theme_templates as ptt
import plotly.express as px


def initData(data, selected, k, peak, top):
    process = Processing(data, selected, k, peak, top)
    return process


def getAlignmentData(process):
    return KMerAlignmentData.processData(process)


def getScatterPlot(process):
    result = KMerScatterPlotData.processData(process)
    df = result[0]
    label = result[1]
    fileNames = result[2]

    fig = px.scatter(df, x=fileNames[0], y=fileNames[1], hover_name=label,
                     color='highlight',
                     color_discrete_map={"TOP {}-mer".format(process.getSettings().getK()): "red",
                                         "{}-mer".format(process.getSettings().getK()): "black"},
                     title='Scatterplot of k-Mer occurences (#)',
                     opacity=0.55,
                     size="size_score",
                     hover_data={'highlight': False, fileNames[0]: True, fileNames[1]: True, 'size_score': False},
                     )
    fig.update_layout(dict(template=ptt.custom_plot_template, legend=dict(title=None)),
                      title=dict(font_size=20))
    fig.update_xaxes(title="#k-Mer of " + fileNames[0], title_font=dict(size=15))
    fig.update_yaxes(title="#k-Mer of " + fileNames[1], title_font=dict(size=15))
    return fig


def getPCA(process):
    pca_dfs = KMerPCAData.processData(process)
    pca_df1 = pca_dfs[0]
    pca_df2 = pca_dfs[1]

    prop = pca_dfs[4].Frequency  # highlighting property Frequency
    propName = prop.name
    figures = []
    for p in [pca_df1, pca_df2]:
        fig = px.scatter(p, x='PC1', y='PC2', hover_name=p.index.tolist(),
                         color=prop,
                         color_continuous_scale='plasma',
                         hover_data={"PC1": True, "PC2": True})
        fig.update_layout(coloraxis_colorbar=dict(
            title=propName,
        ), template=ptt.custom_plot_template, xaxis=dict(zeroline=False, showline=True),
            yaxis=dict(zeroline=False, showline=True))
        fig.update_xaxes(title_font=dict(size=15))
        fig.update_yaxes(title_font=dict(size=15))
        figures.append(fig)
        prop = pca_dfs[5].Frequency

    return figures