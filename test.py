from fastmcp import FastMCP
import os
import sqlite3

DB_PATH=os.path.join(os.path.dirname(__file__),"express.db")

CATEGORIES_PATH=os.path.join(os.path.dirname(__file__),"categories.json")

mcp=FastMCP(name="expensetracker")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
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

def list_expenses(start_date, end_date):
    '''List all expense from date range'''

    with sqlite3.connect(DB_PATH) as conn:
        cur=conn.execute(
            """
            select id,date,amount,category,sub_category,note from express
            where date between ? and ?
            order by id asc
            """,
            (start_date,end_date)
        )
        cols=[col[0] for col in cur.description]
        return [dict(zip(cols,row)) for row in cur.fetchall()]
    
    def summarize(start_date, end_date, category=None):
        """Summarize expenses by category within an inclusive date range."""
    
    
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    


if __name__=="__main__":
    mcp.run()


    
