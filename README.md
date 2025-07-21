I suck

anyways here's all the modifications you can make in user.json and main.py:
***
main.py
| Keys | Comments | Parameters |
|------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------|
| iteration | How many iterations to run, Higher = more accurate but slower | int;0+ |
| rate_up4 | Characters that can be rate-up in 4-star pools | idk |
***
user.json
| Keys | Comments | Parameters |
|------------------|----------------------------------------------------------------------------------------|-------------------------------------------------------|
| wanted_characters | Number of characters you want | int;0+ |
| wanted_weapons | Number of weapons you want | int;0+ |
| wishes | Number of wishes you have | int;0+ |
| starglitter | Amount of starglitter you have | int;0+ |
| radiance | Radiance Level, how  many 5050 lost in a row | int;0-3 | 
| epitomized | Epitomized Weapon System | boolean;True/False | 
| character/5pity | 5-star character pity counter | int;0+ |
| character/5guarantee | Whether the next 5-star character is guaranteed | boolean;True/False |
| character/4pity | 4-star character pity counter | int;0+ |
| character/4guarantee | Whether the next 4-star character is guaranteed | boolean;True/False |
| weapon/5pity | 5-star weapon pity counter | int;0+ |
| weapon/5guarantee | Whether the next 5-star weapon is guaranteed | boolean;True/False |
| weapon/4pity | 4-star weapon pity counter | int;0+ |
| weapon/4guarantee | Whether the next 4-star weapon is guaranteed | boolean;True/False |
| standard | Standard characters Dictionary, put how many copies you have of them, 1 being C0 | int;0-7 | 
| standard | 4* characters Dictionary, put how many copies you have of them, 1 being C0 | int;0-7 | 
***

