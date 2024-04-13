from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://sql8697943:2HSgWDVuLg@sql8.freemysqlhosting.net/sql8697943?charset=utf8mb4")



def load_from_accounts_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from accounts"))
    accounts = []
    for row in result.all():
      accounts.append(row._asdict())
  


  

  