# Motivation for object-based templating engine:
# 1. Easier to reuse fragments, partial attribute lists, and contents, e.g. you can build custom attribute sets
#           - we could define the + operator for attribute objects that combines them, e.g. a(attributes=blue_border + red_fill)
#           - we could "curry" fragments
# 2. Easier to document fragments by leveraging docstring extractors for example
# 3. Easier to spot argument mismatches because static analysers can immediately tell if an argument has not been passed in for a fragment's constructor, for e.g.
#    instead of waiting until rendering.
# 4. Less boilerplate, e.g. div(H1(text) for text in list) rather than <div>{for :text: in :list:}<h1>{text}</h1></div> for e.g.
# 5. Easier to unit test fragments or whatever abstractions you've made

# General idea of an element
# Constructor:
# element(attributes: dict[str, str] | None = None, *content)
# the content would be generators of elements, or elements, or strings.
# Elements must have some to string method which we can use

# *args (h1, h2 in div)
fragment = (
    div(
        h1(
            "Hello"
        ),

        h2(
            "Nice to see you!"
        )
    )
)
# Implicit requirement: tags will be closed when they have content.
# Tags that must have content like h1 and don't have anything will raise an error
# to alert the user that the tag is doing nothing.


# attributes as a keyword arg
# kwargs must be at the end of the parameter list
# so attributes must be the last argument to pass in
#
# attributes is a function to stringify the attributes
# instead of relying on the user
# to pass in a raw dictionary of string-string kv pairs
#
# To extend: inline css can have a similar helper function to convert
# kwargs into "attr1:val1;attr2:val2;"
fragment = (
    a(
        'Visit W3Schools',
        attributes=attributes(
            href='https://www.w3schools.com'
        )
    )
)  # <a href="https://www.w3schools.com">Visit W3Schools</a>


# Users can create their own class-based or function-based fragments
# Also, we can leverage documentation generators for Python for documenting
# templates.
class MyElement(BaseElement):
    """
    This docstring can be extracted by Sphinx to create
    documentation on templates, for example
    """
    pass


def myelem(a, b): return div("hello", a, b)


def MyElem(a, b):
    """
    This docstring can be extracted by Sphinx to create
    documentation on templates, for example
    """
    return div("hello", a, b)


# For accessing static files like images, users should be able to specify
# in the main script the folder name, e.g. _images/ for their images
# e.g.
engine = Engine(images='_images/')
# which checks the existence of the folder
# during initialisation. The keywords are decided by yourself, e.g. calling images 'images'.
# Then you can call engine.images which will return something like an Engine.FileReader
# that takes in a file name, e.g. engine.images['pic1.jpg'] that will then go to that folder
# and search for that picture. This indirection is to allow the engine to throw useful errors,
# e.g. "Folder missing" or "File missing" which would be impossible if we just ask the user
# to pass in the absolute filepath and we just call python's os lib to read it.
my_image = img(
    src=myengine.images['pic1.jpg'], # or url('http://...') which means both objects need to share a superclass, say Resource
    width=500,
    height=800
)
# <img src='_images/pic1.jpg' width="500" height="600">


# To convert the object model into html and to create base elements, we can leverage lxml.html
# The idea is that users can compose fragments like in React
class BlogPost(BaseElement):
    pass

# Can also Pythonise CSS libraries like bootstrap:
# see https://codesandbox.io/s/github/react-bootstrap/code-sandbox-examples/tree/master/basic-react-router
# for how Bootstrap has been JSX-ised.

# Intended usage:
# You define the global state in an Engine object, like static assets' locations.
# You write all your templates in Python files.
# You assemble the object tree in your main script, e.g. root = html(...)
# You run in the terminal [project_name] generate -o output
# The output/ folder can now be served.