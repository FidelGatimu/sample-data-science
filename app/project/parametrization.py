"""Copyright (c) 2022 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from viktor.parametrization import BooleanField
from viktor.parametrization import DownloadButton
from viktor.parametrization import FileField
from viktor.parametrization import MultiSelectField
from viktor.parametrization import NumberField
from viktor.parametrization import OptionField
from viktor.parametrization import Page
from viktor.parametrization import Parametrization
from viktor.parametrization import Text

EXPLANATION_CSV_VISUALIZATION = "## CSV to Matplotlib visualization \nThis is a VIKTOR app that consists of four " \
                                "different pages, all doing something different with data. On top of this page you " \
                                "can see the four different pages. \n\nIn this page it is possible to upload a CSV " \
                                "file. If you want to use an example CSV file you can download one about pokemons by " \
                                "pressing the button below."

EXPLANATION_CSV_PARAMETERS = "After uploading and selecting a CSV file you can plot its data to a Matplotlib using " \
                             "the parameters below."

EXPLANATION_MATPLOTLIB = "After defining the parameters, VIKTOR will plot the data and visualize it in the view on " \
                         "the right. \n\nThe pokemon data was based on data found at " \
                         "[https://abichat.github.io/minesnancy-visu.html]" \
                         "(https://abichat.github.io/minesnancy-visu.html)"

EXPLANATION_PLOTLY = "## Plotly integration \nWith VIKTOR it is super easy to use integrations with other software " \
                     "like Plotly. On the right you can see an interactive plot with build-in data from the plotly" \
                     "library. This is done with just 3 lines of code!"

EXPLANATION_NUMPY = "## Numpy interpolation \nThis example is used to show how you can create interactive apps using " \
                    "VIKTOR. In this example you can pick samples from a sin function. Then use numpy to estimate a " \
                    "interpolation with a given polynomial. Finally, you can check the error at a certain x value. " \
                    "\n\nFirst define the amount of samples below."

EXPLANATION_NUMPY_INTERPOLATION = "Then click on ``Show interpolation`` and define the polynomial."

EXPLANATION_NUMPY_ERROR = "Finally, use the slider below to check the error on certain locations. The error is " \
                           "shown in the data view on the right"

EXPLANATION_PANDAS = "The last example shows how easy you can do data manipulation using VIKTOR. In this page we use " \
                     "the same pokemon database as before. Here the pandas library is used to manipulate data by " \
                     "first removing all data-entries missing a value for its type. Then it creates a corralation " \
                     "matrix used to plot a heatmap.\n\nBelow you can define the types you want to compare. Click " \
                     "on `Select all` to see the full plot. Then press the update button right below."


def get_possible_columns(params, **kwargs):
    """Get all possible column names"""
    if params.csv_page.file_link:
        buffer = params.csv_page.file_link.file.open_binary()
        dataframe = pd.read_csv(buffer)
        buffer.close()
        return dataframe.columns.values.tolist()
    return ['First upload a CSV file']


def get_possible_pokemon_types(params, **kwargs):
    """Get all possible values in type.1 and type.2 column. Excluding NA values"""
    dataframe = pd.read_csv(Path(__file__).parent / 'datasets' / 'pokemon.csv').dropna()
    return sorted(list(set(np.append(dataframe['Type.1'].unique(), dataframe['Type.2'].unique()))))


class ProjectParametrization(Parametrization):
    """Defines the input fields in left-side of the web UI in the Sample entity (Editor)."""
    csv_page = Page('CSV to Matplotlib visualization', views='csv_visualization')
    csv_page.explanation_csv_visualization = Text(EXPLANATION_CSV_VISUALIZATION)
    csv_page.file_link = FileField('CSV file', file_types=['.csv'])
    csv_page.download_button = DownloadButton('Download CSV example', 'download_pokemon_csv')
    csv_page.explanation_csv_parameters = Text(EXPLANATION_CSV_PARAMETERS)
    csv_page.options_x = OptionField('X axis', options=get_possible_columns)
    csv_page.options_y = OptionField('Y axis', options=get_possible_columns)
    csv_page.explanation_matplotlib = Text(EXPLANATION_MATPLOTLIB)

    plotly_express_page = Page('Plotly', views='plotly_visualization')
    plotly_express_page.explanation = Text(EXPLANATION_PLOTLY)

    numpy_interp = Page('Numpy interpolation', views='numpy_interpolate')
    numpy_interp.explanation_numpy = Text(EXPLANATION_NUMPY)
    numpy_interp.linspace = NumberField('Number of samples', min=4, max=15, step=1, default=6, variant='slider')
    numpy_interp.explanation_numpy_interpolation = Text(EXPLANATION_NUMPY_INTERPOLATION)
    numpy_interp.show_graph = BooleanField('Show interpolation')
    numpy_interp.polynomial = NumberField('Polynomial for interpolation', min=0, max=30, step=1, default=8,
                                          variant='slider')
    numpy_interp.explanation_numpy_error = Text(EXPLANATION_NUMPY_ERROR)
    numpy_interp.x = NumberField('X value', min=0, max=6.2, step=0.1, default=0, variant='slider')

    pokemon_pandas = Page('Pokemon with pandas', views='pokemon_type_heat_map')
    pokemon_pandas.explanation = Text(EXPLANATION_PANDAS)
    pokemon_pandas.types = MultiSelectField('Possible pokemon types', options=get_possible_pokemon_types)
