"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2
from flask_debugtoolbar import DebugToolbarExtension

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the list-of-ids-of-melons from the session cart
    # - loop over this list:
    #   - keep track of information about melon types in the cart
    #   - keep track of the total amt ordered for a melon-type
    #   - keep track of the total amt of the entire order
    # - hand to the template the total order cost and the list of melon types

    order_total = 0

    # get the list of melon ids from the session dictionary (cart key), or an 
    # empty list if it doesn't exist
    cart_ids = session.get('cart', [])

    # keep track of melon info in cart dictionary
    cart_dict = {}

    # for every melon id in the cart ids list, if the melon id is in the 
    # cart dictionary, melon info will be bound to the values of a melon
    for melon_id in cart_ids:
        if melon_id in cart_dict:
            melon_info = cart_dict[melon_id]
        # if the melon id is not in the cart dictionary, pull in the melon object
        # and the melon info will be bound to the values of the melon
        else:
            melon_object = melons.get_by_id(melon_id)
            melon_info = cart_dict[melon_id] = {
                'common_name': melon_object.common_name,
                'unit_cost': melon_object.price,
                'qty': 0,
                'total_cost': 0,
            }
        
        # increment quantity and melon subtotal by this melon in cart list
        melon_info['qty'] += 1
        melon_info['total_cost'] += melon_info['unit_cost']

        # increment order total by this melon
        order_total += melon_info['unit_cost']

    # cart variable will be bound to a list of melon values displaying melon info
    cart = cart_dict.values()

    return render_template("cart.html", cart=cart, order_total=order_total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session

    # return "Oops! This needs to be implemented!"

    #if the cart does not exist in the session dictionary, create one
    if 'cart' not in session:
        session['cart'] = []
   
    # add melon's id to the cart list
    session['cart'].append(id)

    # display a confirmation message
    flash("Successfully added to cart.")

    # redirect to /cart page
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.debug = True
    DebugToolbarExtension(app)
    app.run()

