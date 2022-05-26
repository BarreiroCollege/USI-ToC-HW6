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

Open a new browser and **go to [localhost:5000](http://localhost:5000)**. You can directly use that interface to visualize
the problem.

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

## Backend Implementation

## Frontend Implementation
