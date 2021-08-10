from flask import Flask, render_template, request, redirect
import functions as f

app = Flask(__name__)

@app.route("/")
def input():
    """Renders page to input recipes"""
    
    return render_template("input.html")

@app.route("/recipes")
def results():
    """Outputs page containing the highest rated recipe of the desired dish, or outputs error page if 
    the highest rated recipe cannot be found. """

    try: 
        if request.args.get("dishname") == "" or not request.args.get("samplesize").isnumeric():
            return redirect("/") 
        
        else: 
            dishname = request.args.get("dishname")
            dishname = f.recipe_formatter(dishname)
            
            samplesize = request.args.get("samplesize")
            samplesize = int(samplesize)
            
            recipe_links = f.get_recipe_links(dishname, samplesize)
            
            if f.valid_result(recipe_links):
                data = f.get_recipe_data(recipe_links)
                highest_rated = f.highest_rated(data)
                
                if highest_rated == False:
                    return render_template("error.html")
                    
                else:
                    return render_template("results.html", link = highest_rated[0], name = highest_rated[1], rating = highest_rated[2])
                    
            else:
                return render_template("error.html")

    except: 
        return render_template("error.html")