import requests
from bs4 import BeautifulSoup

def recipe_formatter(recipe):
    """Replaces all spaces in the recipe name with a +"""

    recipe_str = ""
    for i in range(len(recipe)): 
        if recipe[i] == " ":
            recipe_str = recipe_str + "+"
        else:
            recipe_str = recipe_str + recipe[i]
    return (recipe_str)

def get_recipe_links(recipe_input, search_size_input):
    """Creates a list of size search_size_input containing all recipes to make recipe_input.
    If it is not possible to return a list of size search_size_input, return all the recipes 
    found on the website.
    """

    link = requests.get('https://www.allrecipes.com/search/results/?search=' + recipe_input).text
    soup = BeautifulSoup(link,'html.parser')
    recipelist = soup.find_all("div", {"class":"card__detailsContainer"})

    recipe_links = []
    i = 0

    while i < search_size_input and i < len(recipelist):    
        r_link = recipelist[i].find("a",{"class":"card__titleLink manual-link-behavior"}).get('href') 
        recipe_links.append(r_link)
        i += 1

    return recipe_links

def valid_result(recipe_links):
    """Returns true if the size of recipe links is greater than 0, and False otherwise"""

    if len(recipe_links) > 0:
        return True
    return False 

def get_recipe_data(recipe_links):
    """Returns a list consisting of dictionaries. Each dictionary consists 
    the link to a recipe, the name of a recipe, and it's rating. If a rating cannot be found,
    the string 'none' will be placed into the dictionary.
    """

    data = []
    for link in recipe_links:
        data_link = requests.get(link).text
        recipe = BeautifulSoup(data_link,'html.parser')
        
        try: 
            name = recipe.find("h1",{"class":"headline heading-content"}).text.replace('\n',"") 
        except:
            name = "None" 
        
        try: 
            input_str = ("component recipe-reviews container-full-width " 
                         "template-two-col with-sidebar-right main-reviews"
                        )
            rating = recipe.find("div",{"class":input_str}).get('data-ratings-average')
        except:
            rating = "None"
        
        recipe_dict = {"link": link, "name": name, "rating": rating}

        data.append(recipe_dict)

    return data 

def highest_rated(data):
    """Returns a tuple consisting of the link to the highest ranked recipe, the name 
    of the highest ranked recipe, and the rating of the highest ranked recipe when possible.
    Otherwise, returns False. 
    """

    highest_link = "" 
    highest_name = ""
    highest_ranking = -1 

    for recipe_dict in data: 
        if recipe_dict["rating"].isnumeric() and float(recipe_dict["rating"]) > float(highest_ranking):
            highest_link = recipe_dict["link"]
            highest_name = recipe_dict["name"]
            highest_ranking = float(recipe_dict["rating"])
    
    if highest_ranking == -1:
        return False 
    
    else:
        return (highest_link, highest_name, highest_ranking)