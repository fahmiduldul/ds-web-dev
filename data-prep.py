import pandas as pd

def get_dataframe():
  '''
  OUTPUT:
  new_df - cleaned dataframe for visualization
  '''
  
  df = pd.read_csv('./dataset/data.csv')

  df = df.drop(columns=['Country Name', 'Country Code', 'Indicator Code'], axis=1)

  desired_row_list = [
    "Mortality rate, infant, male (per 1,000 live births)",
    "GDP (current LCU)",
    "Manufacturing, value added (constant LCU)"
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
    11:"Mortality rate, infant, male (per 1,000 live births)",
    47:"GDP (current LCU)",
    51:"Manufacturing, value added (constant LCU)"
  }

  new_df = new_df.rename(columns=columns_name_map)

  return new_df

