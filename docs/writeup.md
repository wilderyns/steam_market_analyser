# Writeup!

## Introduction

Hello! Here's my off the cuff write up of the development of this application. You'll also find an exported comit log in this docs folder, with full commit history available at: https://github.com/wilderyns/steam_market_analyser

## Planning

Initially I went in with very little plan, as evidenced by the first commit, just had each area of the application - main menu, data display, models, etc - with its own singular file. It quickly became apparent, especially with the scope I had planned, that this was going to become untennable. So I made up the chart on Excalidraw (plan.png) outlining the MVC strcuture and set to work. 

I am notourisouly bad at laying out a formal plan when developing, preferring to dive in, write out a feature, and test on the hoof through trial and error. 

## Development 

Once I'd decided that a more enterprise-esque design (in MVC) was required, I popped everything into Git, more so that if I ruined everything I could always fallback to my original barebones idea. Code from the original files were moved into their new locations and redistributed - models.py split into their respective files, and files like menus.py being split into views and controllers.