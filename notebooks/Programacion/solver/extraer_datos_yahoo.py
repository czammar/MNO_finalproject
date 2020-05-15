import fix_yahoo_finance as yf

def extraer_datos_yahoo(stocks):
  '''
  Funcion para extraer datos de los portafolios de yahoo finance de 2015-01-01 a 2020-04-30
  '''
  df_c = yf.download(stocks, start='2015-01-01', end='2020-04-30').Close
  base = df_c['AAPL'].dropna().to_frame()
  for i in range(0,50):
      base = base.join(df_c.iloc[:,i].to_frame(), lsuffix='_caller', rsuffix='_other')
  base = base.drop(columns=['AAPL_caller'])
  base = base.rename(columns={"AAPL_other": "AAPL"})
  base = base.fillna(method='ffill')
  base = base.fillna(method='bfill')
  return base
