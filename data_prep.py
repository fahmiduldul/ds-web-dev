import pandas as pd
import plotly.graph_objs as go

def get_dataframe():
  '''
  OUTPUT:
  new_df - cleaned dataframe for visualization
  '''
  
  df = pd.read_csv('./dataset/data.csv')

  df = df.drop(columns=['Country Name', 'Country Code', 'Indicator Code'], axis=1)

  desired_row_list = [
    "Mortality rate, infant, male (per 1,000 live births)",
    "GDP (constant 2010 US$)",
    "Manufacturing, value added (constant LCU)",
    "CO2 emissions (kg per 2010 US$ of GDP)"
  ]

  drop_first_and_last_row = [True] * df.shape[1]
  drop_first_and_last_row[0] = False
  drop_first_and_last_row[-1] = False

  desired_df_list = []
  for row_name in desired_row_list:
    temp_df = df[df['Indicator Name'] == row_name].transpose()
    temp_df = temp_df[drop_first_and_last_row]
    desired_df_list.append(temp_df)

  new_df = pd.concat(desired_df_list, axis=1)
  new_df['year'] = new_df.index

  columns_name_map = {
    11:"Mortality rate",
    259:"GDP",
    51:"Manufacturing",
    433:"CO2 Emissions"
  }

  new_df = new_df.rename(columns=columns_name_map)
  return new_df

def get_figures():

  df = get_dataframe()

  # graph 1, line chart GPS & Manufacturing vs Year
  graph_one = []
  desired_columns = ["GDP", "Manufacturing"]
  y_val_df = df[desired_columns]
  x_val = df['year'].tolist()

  #plot data into the figure
  graph_one.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["GDP"].tolist(),
      mode = 'lines+markers',
      name = "GDP"
    )
  )
  graph_one.append(
    go.Scatter(
      x = x_val,
      y = y_val_df["Manufacturing"].tolist(),
      mode = 'lines+markers',
      name = "Manufacturing",
      yaxis = 'y2'
    )
  )

  #figure configuration
  layout_one = dict(
    title = 'GDP & Manufacturing Added Value over Years',
    xaxis = dict(title='Year'),
    yaxis = dict(title='GDP'),
    yaxis2 = dict(title='Manufacturing Added Value', overlaying='y', side='right')
  )

  # figure 2, scatterplot child mortality rate vs GDP
  graph_two = []
  x_val = df['GDP'].tolist()
  y_val = df['Mortality rate'].tolist()

  graph_two.append(
    go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'markers'
    )
  )

  layout_two = dict(
    title='GDP vs Mortality Rate',
    xaxis = dict(title='GDP'),
    yaxis = dict(title='Child Mortality Rate per 1000')
  )

  return [dict(data=graph_one, layout=layout_one), dict(data=graph_two, layout=layout_two)]
