from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://sql8697943:2HSgWDVuLg@sql8.freemysqlhosting.net/sql8697943?charset=utf8mb4")

with engine.connect() as conn:
  result = conn.execute(text("select * from accounts"))
  print('type(result):', type(result))
  result_all = result.all()
  print('type(result.all()):', type(result_all))
  print('result.all():', result_all)

  first_row = result_all[0]
  print(type(first_row))

