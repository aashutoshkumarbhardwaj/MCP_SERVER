from fastmcp import FastMCP
import os
import sqlite3

DB_PATH=os.path.join(os.path.dirname(__file__),"express.db")
mcp=FastMCP(name="expenseLoss")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.cursor("""
                    Create table if not exists express(
                        id integer primary key autoincrement,
                        date text not null,
                        amount real not null,
                        category text not null,
                        sub_category text '',
                        note text default' '
                    
                    )
                    """)
        
    init_db()

@mcp.tool

def add_expense(date,amount,category,sub_category="",note=""):
    '''add a new expense to db'''
    with sqlite3.connect(DB_PATH) as conn:
        cur=conn.execute(
            "insert into express(date,amount,category,sub_category,note) values(?,?,?,?,?)",
            (date,amount,category,sub_category,note)
        )
    

@mcp.tool

def get_expenses():
    with sqlite3.connect(DB_PATH) as conn:
        cur=conn.execute("select id,name,amount,category,sub_category,note from express order by id asc")
        cols=[col[0] for col in cur.description]
        return [dict(zip(cols,row)) for row in cur.fetchall()]

if __name__=="__main__":
    mcp.run
