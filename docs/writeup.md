# Writeup!

The Steam Market Analyser by Al Wilde for HCS501

## Introduction

Hello! Here's my off the cuff write up of the development of this application. You'll also find an exported comit log in this docs folder, with full commit history available at: https://github.com/wilderyns/steam_market_analyser

## Planning

Initially I went in with very little plan, as evidenced by the first commit, just had each area of the application - main menu, data display, models, etc - with its own singular file. It quickly became apparent, especially with the scope I had planned, that this was going to become untennable. So I made up the chart on Excalidraw (plan.png) outlining the MVC strcuture and set to work. 

I am notourisouly bad at laying out a formal plan when developing, preferring to dive in, write out a feature, and test on the hoof through trial and error. 

## Development 

Once I'd decided that a more enterprise-esque design (in MVC) was required, I popped everything into Git, more so that if I ruined everything I could always return to my original barebones idea. Code from the original files were moved into their new locations and redistributed - models.py split into their respective files, and files like menus.py being split into views and controllers.

From there it was a case of taking the areas of the application defined as:

- Main Menu
- Dataset Loading & Viewing
- Dataset
- Filter Application 
- Analysis & Transformation
- Graphing
- Exporting

And building a views, controller, and services for each, modifying the models as needed. The order in which development took place follows the numbering order of the main menu, with dataset viewing first (which required dataset loading), filter application, column selection, transformation and analysis, and graphing. I had intended to split transformation and analysis, however after deciding to move to a more universal way of handling the dataset (such that theoretically any csv dataset could be used) these two closely related features were combined. 

Intercomponenet/service/view/model flows can be seen in appflow.png.

As written, full commit history is available at the project's github, however I have included a commit log generated using https://github.com/sajjad-developer/git-log-html-report. There's a distinct lack of nice git log exporters/viewers akin to what you find on the Github repos commits page, this was the best of the bunch. 

## Documentation Used

The documentation for the core libraries (Rich, Pandas, Numpy) were immensely helpful and are available at:

- Rich: https://rich.readthedocs.io/en/latest/introduction.html
- Pandas: https://pandas.pydata.org/docs/
- Numpy: https://numpy.org/doc/2.4/

