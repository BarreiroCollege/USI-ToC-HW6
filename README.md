# Fashion Store

**Dress a manequin** with a **set of predefined rules** and an **input of clothes** using a **SAT solver**.

## Install & Run

In this section both installation and running is described.

### Prerequisites

Only one prerequisite is required to run the project:

- **Python 3.6**, or higher

Please follow the instructions in the [Python official downloads page](https://www.python.org/downloads/).

### Setup

1. Clone (or download) the repository.

2. (_Optional_) Create a virtual environment, and activate it.  
_This is highly recommended, so all dependencies are isolated from the rest of the Python installation._  
_Help Docs: [Creating virtual environments](https://docs.python.org/3/library/venv.html#creating-virtual-environments)_

3. Install the needed **requirements** from the `requirements.txt` file:  
```shell
pip install requirements.txt
```

Now the project is ready to run. Two options are available: running it from a **script**, or from the **web interface**.

### Web Interface

To **launch the web interface**, just run the following command:

```shell
flask run
```

Open a new browser and **go to [localhost:5000](http://localhost:5000)**. You can directly use that interface to
visualize the problem.

### Script

You may want to take a look at the **example script available at `main.py**`.

1. Import `from store import FashionStore`.
2. Create a new `store = FashionStore()` object (no params). It will automatically parse the `data/wardrobe.json` file
   with all the available garments, colors and constraints.
3. Add the clothes you want to combine in the manequin:
    1. Use the `store.parse_clothes(text)` method, where `text` is a string with lines with the `garment,color` format.
    2. Use the `store.add_cloth(garment, color)` method, where `garment` is a `Garment` object and `color` is a `Color`
       object.
4. Invoke the `dresses = store.dress()` method.

Now the `dresses` object will contain a list with all the available dresses. A dress is identified with a list of
`Cloth` objects, which contain both a `Garment` and a `Color`.

## Problem Description

The basic idea of this problem is that we have a fashion store, and we need to **dress our mannequin**. To do that we
have a **set of colored garments** (a "_cloth_"), and we need to find a combination.  
Since this problem is very loosely defined, we need to come up with constraints and with an appropriate problem size.

First we have to **define the two set of _colors_ ($C$) and _garments_ ($G$)**:

* $C = \\{ \textrm{Red}, \textrm{Blue}, \textrm{Cyan}, \textrm{Green}, \textrm{Yellow}, \textrm{Orange}, \textrm{Purple}, \textrm{White}, \textrm{Grey}, \textrm{Black} \\}$
* $G = \\{ \textrm{Hat}, \textrm{Cap}, \textrm{Umbrella}, \textrm{T-Shirt}, \textrm{Shirt}, \textrm{Top}, \textrm{Jacket}, \textrm{Tie}, \textrm{Gloves}, \textrm{Shorts}, \textrm{Jeans}, \textrm{Pants}, \textrm{Skirt}, \textrm{Tennis}, \textrm{Moccasin}, \textrm{Ice-Skates} \\}$

Given this two sets we needed to **create some constraints** over them that will always be added. They are hardcoded as
they specify, for instance, which garments (or colors) should or should not go together, and we have worked out these
constraints with the following boolean expression:

| Boolean expression                                   | Constrain                                                    |
|------------------------------------------------------|--------------------------------------------------------------|
| $\neg(\textrm{Hat} \wedge \textrm{Cap})$             | You can't wear an Hat and a Cap at the same time             |
| $\neg(\textrm{T-Shirt} \wedge \textrm{Shirt})$       | You can't wear a T-Shirt and a Shirt at the same time        |
| $\neg(\textrm{T-Shirt} \wedge \textrm{Top})$         | You can't wear a T-Shirt and a Top at the same time          |
| $\neg(\textrm{Gloves} \wedge \textrm{Gauntlet})$     | You can't wear Gloves and Gauntlet at the same time          |
| $\neg(\textrm{Shorts} \wedge \textrm{Jeans})$        | You can't wear Shorts and Jeans at the same time             |
| $\neg(\textrm{Shorts} \wedge \textrm{Pants})$        | You can't wear Shorts and Pants at the same time             |
| $\neg(\textrm{Shorts} \wedge \textrm{Skirt})$        | You can't wear Shorts and a Skirt at the same time           |
| $\neg(\textrm{Jeans} \wedge \textrm{Pants})$         | You can't wear Jeans and Pants at the same time              |
| $\neg(\textrm{Jeans} \wedge \textrm{Skirt})$         | You can't wear Jeans and a Skirt at the same time            |
| $\neg(\textrm{Pants} \wedge \textrm{Skirt})$         | You can't wear Pant and a Skirt at the same time             |
| $\neg(\textrm{Tennis} \wedge \textrm{Moccasin})$     | You can't wear Tennis shoes and Mocassin at the same time    |
| $\neg(\textrm{Tennis} \wedge \textrm{Ice-Skates})$   | You can't wear Tennis shoes and Ice-Skates at the same time  |
| $\neg(\textrm{Moccasin} \wedge \textrm{Ice-Skates})$ | You can't wear Moccasin and Ice-Skates at the same time      |
| $\neg(\textrm{Red} \wedge \textrm{Blue})$            | You can't wear one Red and one Blue garment at the same time |
| $\neg(\textrm{Orange} \wedge \textrm{Green})$        | You can't wear one Red and one Blue garment at the same time |
| $\neg(\textrm{Green} \wedge \textrm{Grey})$          | You can't wear one Red and one Blue garment at the same time |
| $\textrm{Tie} \rightarrow \textrm{Shirt}$            | You must wear a Shirt under a Tie                            |
| $\textrm{Gloves} \rightarrow \textrm{Jacket}$        | You must wear a Jacket if you are wearing Gloves             |
| $\textrm{Gauntlet} \rightarrow \textrm{Jacket}$      | You must wear a Jacket if you are wearing Gaunlet            |
| $\textrm{Jacket} \rightarrow \textrm{Jeans}$         | You must wear Jeans if you are wearing a Jacket              |

After that we need to go over the input, made of pairs of a garment and a color, and create the final constrains as
explained in the **[Store](#store) section of the Backend Implementation**.

## Backend Implementation

The _backend_ of the project can be understood as the **implementation of the logical project**. This has been done in
**Python**, aided by the **`z3-solver` library**.  
**Object-oriented programming has been used** to ease access to data in the entire project.

### Models

The **`models.py` file has all the needed classes**.

There is an abstract `BaseModel` class that is later inherited by both `Color` and `Garment`.

Both `Color` and `Garment` classes are quite similar. They both have **an ID** and **a _fancy_ name**, but `Garment` has
an aditional `z-index` field (used later by the frontend). They also both generate an **internal `Bool` object** that is
used by `z3` (it has the `type_X` format, where `type` is either `color` or `garment`, and `X` is the ID).

And the last class, `Cloth`, **has both a `Garment` and a `Color`** (so it can be seen as a tuple of these). But it also
generates "_two_" `Bool` objects: one that is the **_raw_ `Bool`** (with format `cloth_C_G`, where `G` is the color name
and `g` is the garment name), and another one as a **"_rule_" which is the implication of this `Bool` with the
conjunction of both garment and color** (`Implies(cloth_C_G, And(garment.to_bool(), color.to_bool()))`).

### Store

Finally, after defining the models, only the fashion store is missing. For such purpuse, **the `store.py` contains a
`FashionStore` class.**

When creating a new instance of this class, it will **automatically parse the `data/wardrobe.json` file**. This file
shall contain a **list of supported garments**, a **list of supported colors**, and **all the constraints**.  
Regarding the constraints, there can be multiple types of constraints, but they must define which object they target
(_garments_ or _colors_), the type of rules (_negation_ or _implication_), and a list of target values.

Once a new object has been created, two methods can be called to add _available clothes_: either `add_cloth` or
`parse_clothes`. Internally, **clothes are stored in a dictionary**, where the **key is a `Garment`** object and the
**value is a list of `Color`** (so it is possible to support multiple colors for a given garment).  
`add_cloth` will receive a `Cloth` object, and will decompose it into the garment and color. They will be appended to
the dictionary once confirmed that they are both supported.  
`parse_clothes` may be used after reading a text file with the **format `garment,color`**. It will go through all lines
and, if it matches the format and both garment and color are supported, will append the respective cloth to the
dictionary.

Finally, the `dress` method will generate all possible permutations of garments with the list of colors. It will create
a **new `Solver` object for each possible permutation**. This `Solver` object is populated as follows:

* All the **constraint rules** as defined in the `data/wardrobe.json` file.
* A **bidirectional implication to target cloth with garment and color**. As this is not natively supported by `Z3`, it
  was implemented with three different subrules:
    * For each cloth that is "available" in the permutation, the following rule:
        * `Implies(cloth, And(cloth.garment, cloth.color))`
        * _"Picking this cloth implies picking both its garment and color"_
    * For each garment used in any cloth, the following rule:
        * `Implies(garment, Or(cloth1_with_garment, cloth2_with_garment, ...))`
        * _"Picking this garment implies picking any of the available clothes that are using it"_
    * For each color used in any cloth, the following rule:
        * `Implies(color, Or(cloth1_with_color, cloth2_with_color, ...))`
        * _"Picking this color implies picking any of the available clothes that are using it"_
* All available clothes wrapped in an `Or`:
    * `Or(cloth1, cloth2, cloth3, cloth4, ...)`
    * _"Any of these clothes are available to be picked"_

It will return a **list of available dresses**. This list will have a minimum size of 0 (if it cannot be solved), up to
the number of permutations (if all permutations can be solved).  
Thus, each dress will contain a list of `Cloth` object ("_non-conflicting clothes_").

## Frontend Implementation

In order to make the frontend, first we started by writing HTML/CSS templates.
Then, we connected the frontend to the backend using Flask.

### HTML/CSS

For the template, we chose a very simplistic design, with vibrant yet high contrasting colors to make the user
experience more enjoyable.  
The background was done using a css 3d zig-zag pattern found which can be found
[here](https://www.magicpattern.design/tools/css-backgrounds).

### Flask

As mentioned before, we are running flask to connect back end and the front end. The HTML form on the front end POSTs
the form information including the uploaded file to the python script.  
After the execution of the script, the outfits are returned to the frontend through a JSON object and are displayed to
the user.

### Image Models

We are using over 160 image models to display every garment of every color and the recommended outfit to the user.

### Mannequin

In order to visualize the outfits even better, we hired the most handsome model of all time, Diego, to pose with each
and every outfit.  
This was by far the most expensive part of the project.
