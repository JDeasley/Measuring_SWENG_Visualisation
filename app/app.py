from flask import Flask, render_template, url_for
import os
import get_data, cleardb, read_data

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
repos_fetched = []
cleardb.main()

def fetch_data(repo_name):
    if repo_name in repos_fetched:
        print("\nAlready fetched repo: ", repo_name)
    else:
        # 1. Try to fetch data from DB for this repo
        print("\nFetching data of users from repo: ", repo_name)

        try:
            get_data.fetch(repo_name)
        except Exception as err:
            raise err

        repos_fetched.append(repo_name)

    rdata = read_data.db_fetch(repo_name)
    return rdata

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/repo/<path:repo_name>")
def show_repo(repo_name):
    try:
        data = fetch_data(repo_name)
        first_user = data[0]["user"]
    except Exception as err:
        error = True
        message = err
        print(err)

    home_url = url_for('index')

    return render_template("repo.html", **locals())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
